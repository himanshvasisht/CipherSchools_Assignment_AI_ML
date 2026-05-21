import time
from datetime import datetime
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

from analysis.centrality import calculate_centrality
from analysis.dependency_graph import build_dependency_graph

from ingestion.clone_repo import clone_repository
from ingestion.file_scanner import scan_source_files

from parsing.parser_router import parse_file

from review.chunk_builder import build_chunks
from review.complexity_analyzer import analyze_complexity
from review.evidence_builder import build_evidence
from review.llm_reviewer import review_with_llm
from review.quality_analyzer import analyze_quality
from review.review_router import prioritize_evidence
from review.security_analyzer import analyze_security
from review.confidence import compute_hybrid_confidence


def log_step(name, start):
    elapsed = time.time() - start
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {name}: {elapsed:.1f}s")


def validate_github_url(repo_url):
    parsed = urlparse(repo_url.strip())
    if parsed.scheme not in ["http", "https"]:
        return False, "Invalid GitHub URL"

    if parsed.netloc.lower() != "github.com":
        return False, "Only GitHub repository URLs allowed"

    parts = [p for p in parsed.path.split("/") if p]
    if len(parts) < 2:
        return False, "Invalid GitHub repository URL"

    return True, ""


def process_review(ev):
    use_llm = ev.get("use_llm", True)

    try:
        llm_confidence = 80
        agent_agreement = 90
        
        repaired_code = ""
        if use_llm:
            llm_response = review_with_llm(ev)
            if isinstance(llm_response, dict):
                llm_review = llm_response.get("review", "Review unavailable")
                repair = llm_response.get("repair", "Review unavailable")
                repaired_code = llm_response.get("repaired_code", "")
                llm_confidence = llm_response.get("llm_confidence", 80)
                agent_agreement = llm_response.get("agent_agreement", 90)
            else:
                llm_review = "AI review unavailable"
                repair = "Repair unavailable"
        else:
            llm_review = (
                f"Tool-only analysis | "
                f"Risk: {ev['risk_score']} | "
                f"Security: {len(ev['security_report'])} findings"
            )
            repair = "Tool-only routing"

        # Compute final hybrid confidence score
        confidence_value = compute_hybrid_confidence(
            complexity=ev.get("complexity", []),
            security_report=ev.get("security_report", []),
            quality_report=ev.get("quality_report", ""),
            centrality_score=ev.get("centrality", 0),
            llm_confidence=llm_confidence if use_llm else 0,
            agent_agreement=agent_agreement if use_llm else 0
        )

        verify_flag = True if confidence_value < 40 else False

        return {
            "name": ev["name"],
            "type": ev["type"],
            "file": ev["file"],
            "risk_score": ev["risk_score"],
            "confidence": confidence_value,
            "verify": verify_flag,
            "security": ev["security_report"],
            "pylint": ev["quality_report"][:500],
            "code_preview": ev["source"][:500],
            "llm_review": llm_review,
            "repair_suggestions": repair,
            "repaired_code": repaired_code
        }

    except Exception as e:
        print(f"Review error: {e}")
        return {
            "name": ev["name"],
            "type": ev["type"],
            "file": ev["file"],
            "risk_score": ev["risk_score"],
            "confidence": 0,
            "verify": True,
            "security": ev["security_report"],
            "pylint": ev["quality_report"][:500],
            "code_preview": ev["source"][:500],
            "llm_review": "Review unavailable",
            "repair_suggestions": "Repair unavailable",
            "repaired_code": ""
        }


def run_review(repo_url):
    start_time = time.time()

    print("\n" + "=" * 60)
    print(f"Starting review: {repo_url}")
    print("=" * 60)

    try:
        # URL Validation
        valid, msg = validate_github_url(repo_url)
        if not valid:
            return {
                "success": False,
                "error": msg
            }

        # Clone
        clone_start = time.time()
        clone_result = clone_repository(
            repo_url,
            "test_repo",
            timeout_sec=300
        )
        log_step("Clone", clone_start)

        if not clone_result.get("success"):
            return {
                "success": False,
                "error": str(clone_result.get("error", "Clone failed"))
            }

        # Scan
        scan_start = time.time()
        files = scan_source_files(clone_result["path"])
        log_step("Scan", scan_start)

        if not files:
            return {
                "success": False,
                "error": "No source files found"
            }

        print(f"Files: {len(files)}")

        # Parse + Chunk
        parse_start = time.time()

        def parse_and_chunk(file_info):
            try:
                parsed = parse_file(file_info)
                if parsed.get("error"):
                    return None
                chunks = build_chunks(
                    parsed,
                    file_info["path"],
                    parsed.get("raw_source")
                )
                return parsed, chunks
            except Exception:
                return None

        parsed_results = []
        all_chunks = []

        with ThreadPoolExecutor(max_workers=6) as ex:
            results = ex.map(parse_and_chunk, files)

        for result in results:
            if result:
                parsed, chunks = result
                parsed_results.append(parsed)
                all_chunks.extend(chunks)

        log_step("Parse+Chunk", parse_start)
        print(f"Chunks: {len(all_chunks)}")

        # Graph
        graph_start = time.time()
        dependency_graph = build_dependency_graph(files, parsed_results)
        centrality_scores = calculate_centrality(dependency_graph)
        log_step("Dependency Graph", graph_start)

        # Risk Routing
        risk_start = time.time()
        candidates = []

        for chunk in all_chunks:
            complexity = analyze_complexity(chunk["source"])
            complexity_score = sum(c.get("complexity", 0) for c in complexity)
            centrality = centrality_scores.get(chunk["file"], 0)
            risk = complexity_score + centrality

            candidates.append({
                "chunk": chunk,
                "complexity": complexity,
                "risk": risk,
                "centrality": centrality
            })

        candidates = sorted(
            candidates,
            key=lambda x: x["risk"],
            reverse=True
        )[:20]
        log_step("Risk Routing", risk_start)

        # Evidence
        evidence_start = time.time()
        final_evidence = []

        for item in candidates:
            chunk = item["chunk"]
            evidence = build_evidence(
                chunk,
                item["complexity"],
                analyze_quality(chunk["source"]),
                analyze_security(chunk["source"]),
                centrality=item["centrality"]
            )
            final_evidence.append(evidence)

        top_reviews = prioritize_evidence(
            final_evidence,
            top_k=2
        )
        log_step("Evidence", evidence_start)

        # Review
        review_start = time.time()
        with ThreadPoolExecutor(max_workers=2) as ex:
            review_results = list(ex.map(process_review, top_reviews))
        log_step("Review", review_start)

        runtime = round(time.time() - start_time, 2)
        print("=" * 60)
        print(f"Completed in {runtime}s")
        print("=" * 60)

        return {
            "success": True,
            "repo": repo_url,
            "files_scanned": len(files),
            "chunks": len(all_chunks),
            "dependency_nodes": len(dependency_graph),
            "reviews": review_results,
            "runtime_sec": runtime
        }

    except Exception as e:
        print(f"Fatal error: {e}")
        return {
            "success": False,
            "error": str(e)
        }
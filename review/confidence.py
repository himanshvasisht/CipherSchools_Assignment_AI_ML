def compute_static_confidence(complexity, security_report, quality_report):
    """
    Computes static analysis confidence contribution (0-100).
    Base is 100, penalized for security, quality, and complexity issues.
    """
    score = 100
    
    # Penalize for security issues
    security_count = 0
    if isinstance(security_report, list):
        for item in security_report:
            if isinstance(item, dict) and item.get("error"):
                continue
            security_count += 1
    score -= min(security_count * 25, 60)

    # Penalize for lint/quality warnings
    quality_text = str(quality_report).lower()
    quality_findings = any(
        kw in quality_text for kw in ["warning", "error", "convention", "refactor", "unused"]
    )
    if quality_findings:
        score -= 20

    # Penalize for complexity
    complexity_score = sum(
        item.get("complexity", 0) for item in complexity if isinstance(item, dict)
    )
    score -= min(int(complexity_score * 2), 20)

    return max(0, min(100, score))


def compute_hybrid_confidence(
    complexity,
    security_report,
    quality_report,
    centrality_score=0,
    llm_confidence=80,
    agent_agreement=100
):
    """
    Calculates final confidence score using a hybrid formula:
    - 40% Static Analysis (Bandit, Radon, Pylint)
    - 25% Dependency Evidence (Centrality)
    - 20% Multi-Agent Agreement
    - 15% LLM Reasoning Confidence
    """
    # 1. Static Analysis Score (0-100)
    static_score = compute_static_confidence(complexity, security_report, quality_report)

    # 2. Dependency Score (0-100)
    # Higher centrality -> higher dependency evidence (more files import/connect to it)
    dep_score = min(100, int(centrality_score * 10) + 50)

    # 3. Agent Agreement (0-100)
    # Passed in based on agent reviews
    agreement_score = max(0, min(100, agent_agreement))

    # 4. LLM reasoning (0-100)
    llm_score = max(0, min(100, llm_confidence))

    # Weighted sum
    final_score = (
        0.40 * static_score +
        0.25 * dep_score +
        0.20 * agreement_score +
        0.15 * llm_score
    )

    return int(max(0, min(100, final_score)))
from review.confidence import compute_static_confidence


def build_evidence(
    chunk,
    complexity,
    quality,
    security,
    centrality=0
):

    # Compute initial static confidence
    static_conf = compute_static_confidence(
        complexity,
        security,
        quality
    )

    evidence = {
        "type": chunk["type"],
        "name": chunk["name"],
        "file": chunk["file"],
        "source": chunk["source"],
        "complexity": complexity,
        "quality_report": quality,
        "security_report": security,
        "centrality": centrality,
        "risk_score": calculate_risk_score(
            complexity,
            quality,
            security,
            centrality
        ),
        "confidence": static_conf
    }

    return evidence


def calculate_risk_score(
    complexity,
    quality,
    security,
    centrality=0
):

    score = 0

    # Complexity
    for item in complexity:
        score += item.get(
            "complexity",
            0
        )

    # Centrality (highly central files are higher risk)
    score += int(centrality * 10)

    # Pylint
    q = str(quality).lower()

    if "unused" in q:
        score += 2

    if "missing-docstring" in q:
        score += 1

    if "too-many-branches" in q:
        score += 5

    if "too-many-locals" in q:
        score += 4

    # Security
    for issue in security:

        severity = issue.get(
            "issue_severity",
            ""
        ).upper()

        if severity == "LOW":
            score += 5

        elif severity == "MEDIUM":
            score += 10

        elif severity == "HIGH":
            score += 20

    return min(score, 100)
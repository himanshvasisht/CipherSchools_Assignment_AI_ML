from radon.complexity import cc_visit


def analyze_complexity(source_code):
    try:
        blocks = cc_visit(source_code)

        results = []

        for block in blocks:
            results.append({
                "name": block.name,
                "complexity": block.complexity,
                "rank": block.letter
            })

        return results

    except Exception:
        return []
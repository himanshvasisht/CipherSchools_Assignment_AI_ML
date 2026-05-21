def prioritize_evidence(
    evidence_list,
    top_k=2
):
    """
    Smart routing: Top1 gets full LLM review,
    Top2 gets tool-only summary (no LLM call).
    
    Args:
        evidence_list: list of evidence dicts
        top_k: number of items to return (default 2)
               - Top 1: Full AI review (LLM)
               - Top 2: Tool-only summary (no LLM)
    
    Returns:
        List of evidence items with metadata
        about whether LLM should be called.
    """

    sorted_items = sorted(
        evidence_list,
        key=lambda x: x.get(
            "risk_score",
            0
        ),
        reverse=True
    )

    top_items = sorted_items[:top_k]
    
    # Add metadata about LLM usage
    result = []
    for idx, item in enumerate(top_items):
        
        item_with_meta = item.copy()
        
        # Only Top1 uses LLM
        item_with_meta["use_llm"] = (
            idx == 0
        )
        
        result.append(
            item_with_meta
        )
    
    return result
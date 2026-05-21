import json
import re

def build_repair_prompt(code, language, quality_issues, security_issues, arch_issues):
    return f"""
You are an expert Code Repair Agent. Take the original code and the findings from our specialized agents, and produce a repaired/refactored version of the code that resolves the issues.

Original Code:
{code}

Specialized Agent Findings:
- Quality Agent: {quality_issues}
- Security Agent: {security_issues}
- Architecture Agent: {arch_issues}

You MUST respond ONLY with a valid JSON object matching this schema:
{{
    "repair_suggestion": "brief description of top fix",
    "repaired_code": "repaired code snippet",
    "effort": "low, medium, or high",
    "priority": "low, medium, or high",
    "llm_confidence": 85
}}
Ensure the response contains ONLY raw JSON and no markdown code blocks or wrapper text.
"""

def run_repair_agent(code, language, quality_issues, security_issues, arch_issues, provider):
    """
    Synthesizes findings and outputs suggested fix, effort, priority, and self-confidence.
    """
    prompt = build_repair_prompt(code, language, quality_issues, security_issues, arch_issues)
    response = provider.generate(prompt)

    # Clean response in case LLM wrapped it in markdown code blocks
    cleaned = response.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    if cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()

    try:
        data = json.loads(cleaned)
        return data
    except Exception as e:
        print(f"Failed to parse repair agent JSON: {e}. Raw: {response}")
        # Graceful fallback
        return {
            "repair_suggestion": "Clean and refactor original code structure.",
            "repaired_code": code,
            "effort": "low",
            "priority": "medium",
            "llm_confidence": 70
        }
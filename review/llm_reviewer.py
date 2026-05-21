import json
from providers.factory import get_llm_client

llm_client = get_llm_client()

def build_multi_agent_prompt(evidence):
    code_short = evidence["source"][:1000]
    pylint_short = str(evidence["quality_report"])[:400]
    security_short = str(evidence["security_report"])[:300]
    centrality = evidence.get("centrality", 0)
    file_path = evidence.get("file", "unknown")
    language = evidence.get("type", "code")

    return f"""
You are acting as a panel of four specialized AI code review agents:
1. **Quality Agent**: Focuses on readability, naming conventions, style, and code smells.
2. **Security Agent**: Focuses on OWASP hazards, hardcoded secrets, injection, and security practices.
3. **Architecture Agent**: Focuses on import coupling, modularity, and dependency issues.
4. **Repair Agent**: Compiles findings and suggests a repaired/refactored version of the code.

CONTEXT:
File Path: {file_path}
Language/Type: {language}
Centrality Weight: {centrality}
Static Lint: {pylint_short}
Static Security: {security_short}

Code to analyze:
{code_short}

Analyze the code from the perspective of each agent.
You MUST output ONLY a valid JSON object matching the following structure. Do not add markdown blocks or wrapping text:
{{
    "quality_findings": "2-3 bulleted quality findings.",
    "security_findings": "2-3 bulleted security findings or 'No security issues found.'",
    "architecture_findings": "2-3 bulleted dependency/architecture findings or 'No architectural issues found.'",
    "repair_suggestion": "brief explanation of fix",
    "repaired_code": "repaired code snippet",
    "effort": "low/medium/high",
    "priority": "low/medium/high",
    "llm_confidence": 85,
    "agent_agreement": 90
}}
"""

def review_with_llm(evidence):
    """
    Executes a single unified LLM call simulating the multi-agent panel.
    Returns structured results.
    """
    # Fetch the active client (may reload from env if needed)
    global llm_client
    llm_client = get_llm_client()

    prompt = build_multi_agent_prompt(evidence)
    response = llm_client.generate(prompt)

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
        # Format the response in the way process_review expects:
        review_text = (
            f"### Quality Agent findings:\n{data.get('quality_findings', 'None')}\n\n"
            f"### Security Agent findings:\n{data.get('security_findings', 'None')}\n\n"
            f"### Architecture Agent findings:\n{data.get('architecture_findings', 'None')}"
        )
        
        repair_text = (
            f"**Fix Suggested**: {data.get('repair_suggestion', 'N/A')}\n"
            f"**Priority**: {data.get('priority', 'medium').upper()} | **Effort**: {data.get('effort', 'low').upper()}\n\n"
            f"```python\n{data.get('repaired_code', '')}\n```"
        )

        return {
            "review": review_text,
            "repair": repair_text,
            "repaired_code": data.get("repaired_code", ""),
            "llm_confidence": data.get("llm_confidence", 80),
            "agent_agreement": data.get("agent_agreement", 90)
        }
    except Exception as e:
        print(f"Failed to parse multi-agent JSON: {e}. Raw: {response}")
        # Graceful fallback
        return {
            "review": "AI review temporarily unavailable.",
            "repair": "Repair suggestions unavailable.",
            "repaired_code": "",
            "llm_confidence": 50,
            "agent_agreement": 50
        }
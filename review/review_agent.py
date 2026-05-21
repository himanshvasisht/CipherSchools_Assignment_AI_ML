def build_review_prompt(code, language):
    return f"""
You are an expert Code Quality Agent. Analyze the following {language} code for style, conventions, naming, code smells, and readability issues.
Keep your analysis concise (2-3 sentences max).

Code:
{code}

Output your review as a bulleted list of 2-3 key findings. If there are no issues, state "No quality issues found."
"""

def run_review_agent(code, language, provider):
    """
    Analyzes code for quality and design issues.
    """
    prompt = build_review_prompt(code, language)
    response = provider.generate(prompt)
    return response.strip()

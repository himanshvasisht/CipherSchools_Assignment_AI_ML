def build_security_prompt(code, language, static_issues):
    issues_str = ""
    if static_issues:
        issues_str = f"Static analysis flags: {static_issues}\n"
        
    return f"""
You are an expert Security Agent. Analyze the following {language} code for security vulnerabilities, OWASP hazards, hardcoded secrets, injection risks, or unsafe imports.
{issues_str}
Keep your analysis concise (2-3 sentences max).

Code:
{code}

Output your analysis as a bulleted list of 2-3 key findings. If there are no issues, state "No security vulnerabilities found."
"""

def run_security_agent(code, language, provider, static_issues=None):
    """
    Analyzes code for security risks.
    """
    prompt = build_security_prompt(code, language, static_issues)
    response = provider.generate(prompt)
    return response.strip()

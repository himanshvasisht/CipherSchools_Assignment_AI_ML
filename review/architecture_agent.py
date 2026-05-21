def build_arch_prompt(code, file_path, centrality):
    return f"""
You are an expert Software Architect Agent. Review this code in file '{file_path}' (Centrality Score: {centrality}) for coupling, modularity, and cohesion.
Keep your analysis concise (2-3 sentences max).

Code:
{code}

Output your analysis as a bulleted list of 2-3 key findings. If there are no issues, state "No architectural issues found."
"""

def run_architecture_agent(code, file_path, centrality, provider):
    """
    Analyzes code coupling, imports, and centrality metrics.
    """
    prompt = build_arch_prompt(code, file_path, centrality)
    response = provider.generate(prompt)
    return response.strip()

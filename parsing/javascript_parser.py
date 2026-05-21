import re

def parse_javascript_file(file_path):
    """
    Lightweight, regex-based parsing for JS/TS files.
    Extracts imports, classes, and functions with their source.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()

    result = {
        "imports": set(),
        "classes": [],
        "functions": [],
        "raw_source": source
    }

    # Extract imports
    # Match: import ... from 'module' or require('module')
    import_patterns = [
        r"(?:import|export)\s+.*?\s+from\s+['\"]([^'\"]+)['\"]",
        r"require\s*\(\s*['\"]([^'\"]+)['\"]\s*\)"
    ]
    for pattern in import_patterns:
        for match in re.finditer(pattern, source):
            result["imports"].add(match.group(1))

    # Extract classes (class ClassName ...)
    class_pattern = r"(?:export\s+)?class\s+(\w+)(?:\s+extends\s+\w+)?\s*\{"
    class_matches = list(re.finditer(class_pattern, source))
    
    # Extract functions
    # Matches: function name(...) or const name = (...) => or name(...) { in classes
    func_pattern = r"(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*\([^)]*\)\s*\{"
    func_matches = list(re.finditer(func_pattern, source))

    # Arrow functions: const name = async (...) => {
    arrow_pattern = r"(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\([^)]*\)\s*=>\s*\{"
    arrow_matches = list(re.finditer(arrow_pattern, source))

    lines = source.splitlines()

    # Function to extract bracket-matching block
    def get_block_source(start_idx):
        brace_count = 0
        in_block = False
        end_idx = start_idx
        
        for idx in range(start_idx, len(source)):
            char = source[idx]
            if char == '{':
                brace_count += 1
                in_block = True
            elif char == '}':
                brace_count -= 1
                
            if in_block and brace_count == 0:
                end_idx = idx + 1
                break
        return source[start_idx:end_idx]

    # Process class matches
    for match in class_matches:
        name = match.group(1)
        start_pos = match.start()
        block_source = get_block_source(start_pos)
        result["classes"].append({
            "name": name,
            "source": block_source
        })

    # Process function matches
    for match in func_matches:
        name = match.group(1)
        start_pos = match.start()
        block_source = get_block_source(start_pos)
        result["functions"].append({
            "name": name,
            "source": block_source
        })

    # Process arrow functions
    for match in arrow_matches:
        name = match.group(1)
        start_pos = match.start()
        block_source = get_block_source(start_pos)
        result["functions"].append({
            "name": name,
            "source": block_source
        })

    result["imports"] = list(result["imports"])
    return result

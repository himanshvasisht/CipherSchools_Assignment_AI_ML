MAX_CHARS = 1500


def build_chunks(parsed_data, file_path, raw_source=None):

    chunks = []

    # Function chunks
    for func in parsed_data.get("functions", []):

        source = func.get("source", "")

        if source and len(source) <= MAX_CHARS:

            chunks.append({
                "type": "function",
                "name": func["name"],
                "file": file_path,
                "source": source
            })

    # Class chunks
    for cls in parsed_data.get("classes", []):

        source = cls.get("source", "")

        if source and len(source) <= MAX_CHARS:

            chunks.append({
                "type": "class",
                "name": cls["name"],
                "file": file_path,
                "source": source
            })

    # Fallback module chunk
    if not chunks and raw_source:

        if len(raw_source) <= MAX_CHARS:

            chunks.append({
                "type": "module",
                "name": "module_level_code",
                "file": file_path,
                "source": raw_source
            })

    return chunks
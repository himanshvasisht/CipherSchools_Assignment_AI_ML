from parsing.parser_parser import parse_python_file


def parse_file(file_info):

    language = file_info["language"]

    if language == "python":
        return parse_python_file(file_info["path"])

    return {
        "error": f"Parser not implemented for {language}"
    }
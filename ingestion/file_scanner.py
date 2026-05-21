import os

SUPPORTED_LANGUAGES = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".go": "go"
}


def scan_source_files(repo_path):

    discovered_files = []

    for root, dirs, files in os.walk(repo_path):

        # Skip heavy / irrelevant dirs
        dirs[:] = [
            d for d in dirs
            if d not in [
                ".git",
                "node_modules",
                "__pycache__",
                "venv",
                ".venv"
            ]
        ]

        for file in files:

            ext = os.path.splitext(file)[1]

            if ext in SUPPORTED_LANGUAGES:

                discovered_files.append({
                    "path": os.path.join(root, file),
                    "language": SUPPORTED_LANGUAGES[ext]
                })

    return discovered_files
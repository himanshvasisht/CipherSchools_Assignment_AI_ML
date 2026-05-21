import tempfile
import os
import json
import subprocess


def analyze_security(source_code):

    try:

        # Create temp python file
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False,
            encoding="utf-8"
        ) as f:

            f.write(source_code)
            temp_path = f.name

        # Run Bandit JSON mode
        result = subprocess.run(
            [
                "bandit",
                "-f",
                "json",
                temp_path
            ],
            capture_output=True,
            text=True
        )

        os.unlink(temp_path)

        if result.stdout:

            data = json.loads(
                result.stdout
            )

            return data.get(
                "results",
                []
            )

        return []

    except Exception as e:
        return [{
            "error": str(e)
        }]
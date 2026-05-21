import tempfile
import os
from pylint.lint import Run
from pylint.reporters.text import TextReporter
from io import StringIO


def analyze_quality(source_code):

    try:

        # temp file for pylint
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False,
            encoding="utf-8"
        ) as f:

            f.write(source_code)
            temp_path = f.name

        output = StringIO()
        reporter = TextReporter(output)

        Run(
            [temp_path],
            reporter=reporter,
            exit=False
        )

        result = output.getvalue()

        os.unlink(temp_path)

        return result

    except Exception as e:
        return str(e)
    
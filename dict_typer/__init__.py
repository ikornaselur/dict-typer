import json
import sys
from typing import Dict

from dict_typer.convert import ConvertException, convert


def dict_typer() -> None:
    if sys.stdin.isatty():
        print("Pipe dictionary instance dict-typer")
        sys.exit(1)

    stream = sys.stdin.read().strip()
    show_imports = "--imports" in sys.argv

    try:
        parsed: Dict = json.loads(stream)
    except json.decoder.JSONDecodeError as e:
        raise ConvertException(f"Unable to parse source: {str(e)}")

    try:
        output = convert(parsed, show_imports=show_imports)
    except ConvertException as e:
        print(str(e))
        sys.exit(2)

    print(output)

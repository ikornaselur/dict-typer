import json
from typing import Dict

INDENTATION = 4


class ConvertException(Exception):
    pass


def convert(source: str) -> str:
    try:
        parsed: Dict = json.loads(source)
    except json.decoder.JSONDecodeError as e:
        raise ConvertException(f"Unable to parse source: {str(e)}")

    if not isinstance(parsed, Dict):
        raise Exception("Expected a dictionary")

    root_def = ["class RootType(TypedDict):"]
    for key, value in parsed.items():
        root_def.append(" " * INDENTATION + f"{key}: {type(value).__name__}")

    return "\n".join(root_def)

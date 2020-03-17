import json
from typing import Dict

INDENTATION = 4


def convert(source: str) -> str:
    parsed: Dict = json.loads(source)
    if not isinstance(parsed, Dict):
        raise Exception("Expected a dictionary")

    root_def = ["class RootType(TypedDict):"]
    for key, value in parsed.items():
        print(key, value, type(value))
        root_def.append(" " * INDENTATION + f"{key}: {type(value).__name__}")

    return "\n".join(root_def)

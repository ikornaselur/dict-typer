import json
from typing import Dict, List, Any

INDENTATION = 4
BUILTINS = (str, int, float)


class ConvertException(Exception):
    pass


def _get_type(item: Any) -> Any:
    if isinstance(item, BUILTINS):
        return type(item).__name__

    if isinstance(item, list):
        list_item_types = {_get_type(x) for x in item}
        if len(list_item_types) == 0:
            return "List"
        if len(list_item_types) == 1:
            return f"List[{list_item_types.pop()}]"
        union_type = f"Union[{', '.join(str(t) for t in sorted(list_item_types))}]"
        return f"List[{union_type}]"


def convert(source: str) -> str:
    try:
        parsed: Dict = json.loads(source)
    except json.decoder.JSONDecodeError as e:
        raise ConvertException(f"Unable to parse source: {str(e)}")

    if not isinstance(parsed, Dict):
        raise Exception("Expected a dictionary")

    root_def = ["class RootType(TypedDict):"]
    for key, value in parsed.items():
        root_def.append(" " * INDENTATION + f"{key}: {_get_type(value)}")

    return "\n".join(root_def)

from typing import Any, Dict, Tuple, List

INDENTATION = 4
BUILTINS = (str, bytes, int, float)


class ConvertException(Exception):
    pass


def _get_type(item: Any) -> Any:
    if isinstance(item, BUILTINS):
        return type(item).__name__

    if isinstance(item, (List, Tuple)):
        if isinstance(item, List):
            sequence_type = "List"
        else:
            sequence_type = "Tuple"

        list_item_types = {_get_type(x) for x in item}
        if len(list_item_types) == 0:
            return sequence_type
        if len(list_item_types) == 1:
            return f"{sequence_type}[{list_item_types.pop()}]"
        union_type = f"Union[{', '.join(str(t) for t in sorted(list_item_types))}]"
        return f"{sequence_type}[{union_type}]"


def convert(source: Dict) -> str:
    if not isinstance(source, Dict):
        raise Exception("Expected a dictionary")

    root_def = ["class RootType(TypedDict):"]
    for key, value in source.items():
        root_def.append(" " * INDENTATION + f"{key}: {_get_type(value)}")

    return "\n".join(root_def)

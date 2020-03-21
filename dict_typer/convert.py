from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

INDENTATION = 4
BUILTINS = (str, bytes, int, float, complex)


class ConvertException(Exception):
    pass


class UnknownType(ConvertException):
    pass


@dataclass
class TypedDictDefinition:
    name: str
    members: List[Tuple[str, str]]

    def printable(self) -> str:
        printable_name = f"class {self.name}(TypedDict):"
        printable_members = [
            " " * INDENTATION + f"{key}: {value}" for key, value in self.members
        ]
        return "\n".join([printable_name, *printable_members])


def convert(
    source: Dict, source_type_name: str = "Root", type_postfix: str = "Type"
) -> str:
    if not isinstance(source, Dict):
        raise Exception("Expected a dictionary")

    source_def = _convert_dict(source, source_type_name, type_postfix)

    return source_def.printable()


def _convert_dict(
    source: Dict, root_type_name: str, type_postfix: str
) -> TypedDictDefinition:
    # First pass of base types
    nested = []
    members = []
    for key, value in source.items():
        if isinstance(value, dict):
            nested.append((key, value))
            continue
        members.append((key, _get_type(value)))

    # Second pass of nested dict types
    if nested:
        pass

    return TypedDictDefinition(name=f"{root_type_name}{type_postfix}", members=members)


def _get_type(item: Any) -> Any:
    if isinstance(item, BUILTINS):
        return type(item).__name__

    if isinstance(item, (list, tuple)):
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

    raise UnknownType(item)

from typing import Any, Dict, List, Set, Tuple, Type, Union

from dict_typer.exceptions import ConvertException
from dict_typer.models import MemberDefinition, NestedDictRef, TypedDefinion
from dict_typer.utils import key_to_class_name

BASE_TYPES: Tuple[Type, ...] = (  # type: ignore
    bool,
    bytearray,
    bytes,
    complex,
    enumerate,
    float,
    int,
    memoryview,
    range,
    str,
    type,
    filter,
    map,
    zip,
)


def convert(
    source: Union[Dict, List],
    root_type_name: str = "Root",
    type_postfix: str = "Type",
    show_imports: bool = True,
) -> str:
    if not isinstance(source, (list, dict)):
        raise ConvertException(f"Unsupported source type: {type(source)}")

    source = source.copy()  # Copy the source as it will be modified

    typing_imports: Set[str] = set()
    definitions: List[TypedDefinion] = []
    replacements: Dict[str, str] = {}

    def convert_list(key: str, l: List) -> None:
        type_idx = 0
        for idx, item in enumerate(l):
            if isinstance(item, dict):
                nested_type_name = f"{key_to_class_name(key)}Item{type_postfix}"
                if type_idx:
                    nested_type_name += str(type_idx)

                converted_type_name = convert_dict(nested_type_name, item)

                if converted_type_name == nested_type_name:
                    type_idx += 1

                l[idx] = NestedDictRef(name=converted_type_name)

    def convert_dict(type_name: str, d: Dict) -> str:
        for key, value in d.items():
            if isinstance(value, dict):
                nested_type_name = f"{key_to_class_name(key)}Type"
                convert_dict(nested_type_name, value)
                d[key] = NestedDictRef(name=nested_type_name)
            elif isinstance(value, list):
                convert_list(key, value)

        members: List[MemberDefinition] = []
        for key, value in d.items():
            members.append(MemberDefinition(name=key, types=[get_type(value)]))

        td: TypedDefinion
        type_def = next((td for td in definitions if td.members == members), None)

        if type_def:
            replacements[type_name] = type_def.name
            type_def.update_members(members)
        else:
            type_def = TypedDefinion(name=type_name, members=members)
            definitions.append(type_def)

        typing_imports.update(type_def.get_imports())

        return type_def.name

    def get_type(item: Any) -> Any:
        if item is None:
            return "None"

        if isinstance(item, NestedDictRef):
            return item.name

        if isinstance(item, BASE_TYPES):
            return type(item).__name__

        if isinstance(item, (list, set, tuple, frozenset)):
            if isinstance(item, list):
                sequence_type = "List"
            elif isinstance(item, set):
                sequence_type = "Set"
            elif isinstance(item, frozenset):
                sequence_type = "FrozenSet"
            else:
                sequence_type = "Tuple"

            typing_imports.add(sequence_type)
            list_item_types = {get_type(x) for x in item}
            if len(list_item_types) == 0:
                return sequence_type
            if len(list_item_types) == 1:
                return f"{sequence_type}[{list_item_types.pop()}]"
            if len(list_item_types) == 2 and "None" in list_item_types:
                list_item_types.discard("None")
                typing_imports.add("Optional")
                return f"{sequence_type}[Optional[{list_item_types.pop()}]]"

            union_type = f"Union[{', '.join(str(t) for t in sorted(list_item_types))}]"
            typing_imports.add("Union")
            return f"{sequence_type}[{union_type}]"

        if isinstance(item, dict):
            raise ConvertException(
                "Unable to return type instance of dict, preprocess and use NestedDictDec"
            )

        raise NotImplementedError(f"Type handling for '{type(item)}' not implemented")

    if isinstance(source, dict):
        convert_dict(f"{root_type_name}{type_postfix}", source)
    else:
        convert_list(f"{root_type_name}", source)
        # Run get type to add imports
        get_type(source)

    output = ""

    if show_imports:
        if typing_imports:
            output += "\n".join(
                [f"from typing import {', '.join(sorted(typing_imports))}", "", ""]
            )
        if len(definitions):
            output += "\n".join(["from typing_extensions import TypedDict", "", "", ""])

    output += "\n\n\n".join(d.printable(replacements) for d in definitions)

    if isinstance(source, list):
        # When the root is a list, add a type alias for the list
        if len(output):
            output += "\n"
            if len(definitions):
                output += "\n\n"
        output += f"{root_type_name}{type_postfix} = {get_type(source)}"

    return output

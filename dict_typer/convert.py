from typing import Any, Dict, List, Set, Union

from dict_typer.exceptions import ConvertException
from dict_typer.models import NestedDictDef, TypedDefinion
from dict_typer.utils import key_to_class_name

BUILTINS = (str, bytes, int, float, complex)


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

                l[idx] = NestedDictDef(name=converted_type_name)

    def convert_dict(type_name: str, d: Dict) -> str:
        for key, value in d.items():
            if isinstance(value, dict):
                nested_type_name = f"{key_to_class_name(key)}Type"
                convert_dict(nested_type_name, value)
                d[key] = NestedDictDef(name=nested_type_name)
            elif isinstance(value, list):
                convert_list(key, value)

        members = []
        for key, value in d.items():
            members.append((key, get_type(value)))

        type_def = TypedDefinion(name=type_name, members=members)
        existing = next((td for td in definitions if td == type_def), None)
        if existing:
            replacements[type_name] = existing.name
            return existing.name
        else:
            definitions.append(type_def)
            return type_def.name

    def get_type(item: Any) -> Any:
        if isinstance(item, NestedDictDef):
            return item.name

        if isinstance(item, BUILTINS):
            return type(item).__name__

        if isinstance(item, (list, tuple, set)):
            if isinstance(item, List):
                sequence_type = "List"
            elif isinstance(item, Set):
                sequence_type = "Set"
            else:
                sequence_type = "Tuple"
            typing_imports.add(sequence_type)

            list_item_types = {get_type(x) for x in item}
            if len(list_item_types) == 0:
                return sequence_type
            if len(list_item_types) == 1:
                return f"{sequence_type}[{list_item_types.pop()}]"
            union_type = f"Union[{', '.join(str(t) for t in sorted(list_item_types))}]"
            typing_imports.add("Union")
            return f"{sequence_type}[{union_type}]"

        if item is None:
            return "None"

        raise NotImplementedError(f"Type handling for '{type(item)}' not implemented")

    if isinstance(source, dict):
        convert_dict(f"{root_type_name}{type_postfix}", source)
    else:
        convert_list(f"{root_type_name}", source)
        typing_imports.add("List")

    output = ""

    if show_imports:
        if typing_imports:
            output += "\n".join(
                [f"from typing import {', '.join(sorted(typing_imports))}", "", ""]
            )
        if len(definitions):
            output += "\n".join(["from typing_extensions import TypedDict", "", "", ""])

    output += "\n\n".join(d.printable(replacements) for d in definitions)

    if isinstance(source, list):
        # When the root is a list, add a type alias for the list
        if len(output):
            output += "\n"
            if len(definitions):
                output += "\n"
        output += f"{root_type_name}{type_postfix} = {get_type(source)}"

    return output

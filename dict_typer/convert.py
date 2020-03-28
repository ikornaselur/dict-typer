from typing import Any, Dict, List, Set, Tuple, Union

INDENTATION = 4
BUILTINS = (str, bytes, int, float, complex)


class ConvertException(Exception):
    pass


class UnknownType(ConvertException):
    pass


def key_to_class_name(key: str) -> str:
    return "".join(part[0].upper() + part[1:] for part in key.split("_"))


class TypedDefinion:
    name: str
    members: List[Tuple[str, str]]

    def __init__(self, name: str, members: List[Tuple[str, str]]) -> None:
        self.name = name
        self.members = members

    def printable(self, replacements: Dict[str, str]) -> str:
        output: List[str] = []

        printable_name = f"class {self.name}(TypedDict):"
        printable_members: List[str] = []
        for key, value in self.members:
            if value in replacements:
                value = replacements[value]

            printable_members.append(" " * INDENTATION + f"{key}: {value}")

        output += [printable_name, *printable_members]

        return "\n".join(output)

    def __repr__(self) -> str:
        return f"<TypedDefinion ({self.name})>"

    def __eq__(self, other: Any) -> bool:
        """ Only compares the members and ignores the order """
        if self.__class__ != other.__class__:
            return False
        assert isinstance(other, self.__class__)

        self_members = sorted(self.members)
        other_members = sorted(other.members)

        return self_members == other_members


class NestedDictDef:
    name: str

    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"<NestedDictDef ({self.name})>"


def convert(
    source: Union[Dict, List],
    root_type_name: str = "Root",
    type_postfix: str = "Type",
    show_imports: bool = False,
) -> str:
    if isinstance(source, list):
        raise ConvertException("Convert doesn't support list yet")

    source = source.copy()  # Copy the source as it will be modified

    typing_imports: Set[str] = set()
    definitions: List[TypedDefinion] = []
    replacements: Dict[str, str] = {}

    def convert_dict(type_name: str, d: Dict) -> str:
        for key, value in d.items():
            if isinstance(value, dict):
                nested_type_name = f"{key_to_class_name(key)}Type"
                convert_dict(nested_type_name, value)
                d[key] = NestedDictDef(name=nested_type_name)
            elif isinstance(value, list):
                type_idx = 0
                for idx, item in enumerate(value):
                    if isinstance(item, dict):
                        nested_type_name = f"{key_to_class_name(key)}ItemType"
                        if type_idx:
                            nested_type_name += str(type_idx)

                        converted_type_name = convert_dict(nested_type_name, item)

                        if converted_type_name == nested_type_name:
                            type_idx += 1

                        value[idx] = NestedDictDef(name=converted_type_name)

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

        raise NotImplementedError(f"Type handling for '{type(item)}' not implemented")

    convert_dict(f"{root_type_name}{type_postfix}", source)

    output = ""

    if show_imports:
        if typing_imports:
            output += "\n".join(
                [f"from typing import {', '.join(sorted(typing_imports))}", "", ""]
            )
        output += "\n".join(["from typing_extensions import TypedDict", "", "", ""])

    output += "\n\n".join(d.printable(replacements) for d in definitions)

    return output

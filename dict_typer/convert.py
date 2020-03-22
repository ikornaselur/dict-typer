from typing import Any, Dict, List, Set, Tuple

INDENTATION = 4
BUILTINS = (str, bytes, int, float, complex)


class ConvertException(Exception):
    pass


class UnknownType(ConvertException):
    pass


class TypedDictDefinition:
    name: str
    members: List[Tuple[str, str]]
    nested_defs: List["TypedDictDefinition"]
    _typing_imports: Set[str]

    def __init__(self, root_type_name: str, type_postfix: str, source: Dict,) -> None:
        self.name = f"{root_type_name}{type_postfix}"
        self.members: List[Tuple[str, str]] = []
        self.nested_defs: List[TypedDictDefinition] = []
        self._typing_imports = set()

        # First pass of base types
        nested: List[Tuple[str, Dict]] = []

        for key, value in source.items():
            if isinstance(value, dict):
                nested.append((key, value))
                continue
            self.members.append((key, self._get_type(value)))

        # Second pass of nested dict types
        for nested_key, nested_val in nested:
            nested_def = TypedDictDefinition(
                root_type_name=nested_key.title().replace("_", ""),
                type_postfix=type_postfix,
                source=nested_val,
            )
            existing_def = next((d for d in self.nested_defs if d == nested_def), None)
            if existing_def:
                self.members.append((nested_key, existing_def.name))
            else:
                self.members.append((nested_key, nested_def.name))
                self.nested_defs.append(nested_def)

    def printable(self, show_imports: bool = False) -> str:
        printable_name = f"class {self.name}(TypedDict):"
        printable_members = [
            " " * INDENTATION + f"{key}: {value}" for key, value in self.members
        ]

        output: List[str] = []
        if show_imports:
            output += [
                f"from typing import {', '.join(self.typing_imports)}",
                "",
                "from typing_extensions import TypedDict",
                "",
                "",
            ]

        output += [printable_name, *printable_members]

        if self.nested_defs:
            output += ["\n" + nested_def.printable() for nested_def in self.nested_defs]
        return "\n".join(output)

    @property
    def typing_imports(self) -> List[str]:
        imports = self._typing_imports

        for nested_def in self.nested_defs:
            imports.update(nested_def.typing_imports)

        return sorted(imports)

    def _get_type(self, item: Any) -> Any:
        if isinstance(item, BUILTINS):
            return type(item).__name__

        if isinstance(item, (list, tuple)):
            if isinstance(item, List):
                sequence_type = "List"
            else:
                sequence_type = "Tuple"
            self._typing_imports.add(sequence_type)

            list_item_types = {self._get_type(x) for x in item}
            if len(list_item_types) == 0:
                return sequence_type
            if len(list_item_types) == 1:
                return f"{sequence_type}[{list_item_types.pop()}]"
            union_type = f"Union[{', '.join(str(t) for t in sorted(list_item_types))}]"
            self._typing_imports.add("Union")
            return f"{sequence_type}[{union_type}]"

        raise NotImplementedError(f"Type handling for '{type(item)}' not implemented")

    def __eq__(self, other: Any) -> bool:
        """ Only compares the members and ignores the order """
        if self.__class__ != other.__class__:
            return False
        assert isinstance(other, self.__class__)

        self_members = sorted(self.members)
        other_members = sorted(other.members)

        return self_members == other_members


def convert(
    source: Dict,
    *,
    source_type_name: str = "Root",
    type_postfix: str = "Type",
    show_imports: bool = False,
) -> str:
    if not isinstance(source, Dict):
        raise Exception("Expected a dictionary")

    source_def = TypedDictDefinition(
        root_type_name=source_type_name, type_postfix=type_postfix, source=source
    )

    return source_def.printable(show_imports=show_imports)

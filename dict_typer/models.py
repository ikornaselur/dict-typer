from typing import Any, Dict, List, Optional, Set

from dict_typer.utils import is_valid_key


class MemberDefinition:
    name: str
    types: List[str]

    def __init__(self, name: str, types: Optional[List[str]] = None) -> None:
        self.name = name
        if types:
            self.types = types
        else:
            self.types = []

    def printable_types(self) -> str:
        if len(self.types) == 1:
            return self.types[0]

        if len(self.types) == 2 and "None" in self.types:
            optional_type = (set(self.types) ^ {"None"}).pop()
            return f"Optional[{optional_type}]"

        return f"Union[{', '.join(str(t) for t in sorted(self.types))}]"

    def get_imports(self) -> Set[str]:
        if len(self.types) > 1:
            return {"Union"}
        if len(self.types) == 2 and "None" in self.types:
            return {"Optional"}
        return set()

    def __repr__(self) -> str:
        return f"<MemberDefinition ({self.name}: {self.printable_types()})>"

    def __eq__(self, other: Any) -> bool:
        """ Only compares the member name """
        if self.__class__ != other.__class__:
            return False
        assert isinstance(other, self.__class__)

        return self.name == other.name


class TypedDefinion:
    name: str
    members: List[MemberDefinition]

    def __init__(
        self, name: str, members: List[MemberDefinition], indentation: int = 4
    ) -> None:
        self.name = name
        self.members = members
        self.indentation = indentation

    def any_invalid_key(self) -> bool:
        return any(not is_valid_key(key) for key in self.members_names)

    def printable(self, replacements: Dict[str, str], alternative: bool = False) -> str:
        if alternative or self.any_invalid_key():
            return self._printable_alternative(replacements)
        return self._printable_primary(replacements)

    def _printable_alternative(self, replacements: Dict[str, str]) -> str:
        output: List[str] = []

        printable_name_start = f'{self.name} = TypedDict("{self.name}", {{'
        printable_name_end = "})"

        printable_members: List[str] = []
        for member in self.members:
            for idx, value in enumerate(member.types):
                if value in replacements:
                    member.types[idx] = replacements[value]

            printable_members.append(
                f'{" " * self.indentation}"{member.name}": {member.printable_types()},'
            )

        output += [printable_name_start, *printable_members, printable_name_end]

        return "\n".join(output)

    def _printable_primary(self, replacements: Dict[str, str]) -> str:
        output: List[str] = []

        printable_name = f"class {self.name}(TypedDict):"
        printable_members: List[str] = []
        for member in self.members:
            for idx, value in enumerate(member.types):
                if value in replacements:
                    member.types[idx] = replacements[value]

            printable_members.append(
                f"{' ' * self.indentation}{member.name}: {member.printable_types()}"
            )

        output += [printable_name, *printable_members]

        return "\n".join(output)

    def update_members(self, other_members: List[MemberDefinition]) -> None:
        if self.members != other_members:
            raise Exception("Members don't match")

        for member in other_members:
            existing_member = next(m for m in self.members if m.name == member.name)
            existing_member.types = list(set(existing_member.types) | set(member.types))

    @property
    def members_names(self) -> List[str]:
        return [member.name for member in self.members]

    def get_imports(self) -> Set[str]:
        imports = set()
        for member in self.members:
            imports.update(member.get_imports())
        return imports

    def __repr__(self) -> str:
        return f"<TypedDefinion ({self.name})>"

    def __eq__(self, other: Any) -> bool:
        """ Only compares the members and ignores the order """
        if self.__class__ != other.__class__:
            return False
        assert isinstance(other, self.__class__)

        return set(self.members) == set(other.members)


class NestedDictDef:
    name: str

    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"<NestedDictDef ({self.name})>"

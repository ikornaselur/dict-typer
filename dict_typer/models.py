from typing import Any, Dict, List, Tuple


class TypedDefinion:
    name: str
    members: List[Tuple[str, str]]

    def __init__(
        self, name: str, members: List[Tuple[str, str]], indentation: int = 4
    ) -> None:
        self.name = name
        self.members = members
        self.indentation = indentation

    def printable(self, replacements: Dict[str, str]) -> str:
        output: List[str] = []

        printable_name = f"class {self.name}(TypedDict):"
        printable_members: List[str] = []
        for key, value in self.members:
            if value in replacements:
                value = replacements[value]

            printable_members.append(f"{' ' * self.indentation}{key}: {value}")

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

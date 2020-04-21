from typing import Any, Dict, List, Optional, Set, Union

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


class MemberEntry:
    """ A representation of a type with optional sub types

    A MemberEntry without subtypes can be considered as a leaf of a tree, in
    most cases it will be a simple unit such as str, int, float, but it can
    also be a List, Set, Tuple, Dict without any known members.
    """

    name: str
    sub_members: Set[Union["MemberEntry", "DictEntry"]]

    def __init__(
        self,
        name: str,
        sub_members: Optional[Set[Union["MemberEntry", "DictEntry"]]] = None,
    ) -> None:
        self.name = name
        self.sub_members = sub_members or set()

    def __hash__(self) -> int:
        return hash(str(self))

    def __repr__(self) -> str:
        return f"<MemberEntry ({self})>"

    def __str__(self) -> str:
        def get_member_value(item: Union["MemberEntry", "DictEntry"]) -> str:
            """ Only reference DictEntry by name """
            if isinstance(item, DictEntry):
                return item.name
            return str(item)

        if len(self.sub_members) == 2 and "None" in (
            sm.name for sm in self.sub_members
        ):
            optional_member = next(sm for sm in self.sub_members if sm.name != "None")
            return f"{self.name}[Optional[{get_member_value(optional_member)}]]"
        if len(self.sub_members) > 0:
            sub_members_strs = sorted(get_member_value(sm) for sm in self.sub_members)
            if len(sub_members_strs) == 1:
                return f"{self.name}[{sub_members_strs[0]}]"
            return f"{self.name}[Union[{', '.join(sub_members_strs)}]]"

        return self.name


class DictEntry:
    """ A representation of a typed dict

    A typed dict will have a name and a members map. The value of each member
    is a MemberEntry, which has a name and an optional submembers.
    """

    name: str
    members: Dict[str, MemberEntry]
    indentation: int
    force_alternative: bool

    def __init__(
        self,
        name: str,
        members: Optional[Dict[str, MemberEntry]],
        indentation: int = 4,
        force_alternative: bool = False,
    ) -> None:
        self.name = name
        self.members = members or {}
        self.indentation = indentation
        self.force_alternative = force_alternative

    def __repr__(self) -> str:
        return f"<DictEntry ({self})>"

    def __str__(self) -> str:
        out: List[str] = []

        if self.force_alternative:
            out.append(f'{self.name} = TypedDict("{self.name}", {{')

            for key, value in self.members.items():
                if isinstance(value, DictEntry):
                    out.append(f'{" " * self.indentation}"{key}": {value.name}')
                else:
                    out.append(f'{" " * self.indentation}"{key}": {value}')

            out.append("})")
        else:
            out.append(f"class {self.name}(TypedDict):")
            for key, value in self.members.items():
                if isinstance(value, DictEntry):
                    out.append(f"{' ' * self.indentation}{key}: {value.name}")
                else:
                    out.append(f"{' ' * self.indentation}{key}: {value}")

        return "\n".join(out)


class NestedDictRef:
    name: str

    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"<NestedDictRef ({self.name})>"

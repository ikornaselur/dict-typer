import functools
from typing import Any, Dict, List, Optional, Set, TypeVar

from dict_typer.utils import is_valid_key

KNOWN_TYPE_IMPORTS = ("List", "Tuple", "Set", "FrozenSet")


EntryType = TypeVar("EntryType", "MemberEntry", "DictEntry")
SubMembers = Set[EntryType]
DictMembers = Dict[str, SubMembers]


def is_valid_name(name: str) -> bool:
    if not is_valid_key(name):
        return False
    return name not in KNOWN_TYPE_IMPORTS


def sub_members_to_string(sub_members: SubMembers) -> str:
    def get_member_value(item: EntryType) -> str:
        """ Only reference DictEntry by name. """
        if isinstance(item, DictEntry):
            return item.name
        return str(item)

    if len(sub_members) == 2 and "None" in (sm.name for sm in sub_members):
        optional_member = next(sm for sm in sub_members if sm.name != "None")
        return f"Optional[{get_member_value(optional_member)}]"
    if len(sub_members) > 0:
        sub_members_strs = sorted(get_member_value(sm) for sm in sub_members)
        if len(sub_members_strs) == 1:
            return str(sub_members_strs[0])
        return f"Union[{', '.join(sub_members_strs)}]"
    return ""


def sub_members_to_imports(sub_members: SubMembers) -> Set[str]:
    imports = set()

    for member in sub_members:
        imports |= member.get_imports()

    if len(sub_members) == 2 and "None" in (sm.name for sm in sub_members):
        imports.add("Optional")
    elif len(sub_members) > 1:
        imports.add("Union")

    return imports


class MemberEntry:
    """ A representation of a type with optional sub types.

    A MemberEntry without subtypes can be considered as a leaf of a tree, in
    most cases it will be a simple unit such as str, int, float, but it can
    also be a List, Set, Tuple, Dict without any known members.
    """

    name: str
    sub_members: SubMembers

    def __init__(self, name: str, sub_members: Optional[SubMembers] = None,) -> None:
        self.name = name
        self.sub_members = sub_members or set()

    def get_imports(self) -> Set[str]:
        imports = set()
        if self.name in KNOWN_TYPE_IMPORTS:
            imports.add(self.name)

        return imports | sub_members_to_imports(self.sub_members)

    @property
    def depends_on(self) -> Set[str]:
        return {sm.name for sm in self.sub_members}

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other: Any) -> bool:
        if self.__class__ != other.__class__:
            return False
        assert isinstance(other, self.__class__)

        return str(self) == str(other)

    def __repr__(self) -> str:
        return f"<MemberEntry ({self})>"

    def __str__(self) -> str:
        sub_string = sub_members_to_string(self.sub_members)
        if sub_string:
            return f"{self.name}[{sub_string}]"

        return self.name


class DictEntry:
    """ A representation of a typed dict.

    A typed dict will have a name and a members map. The value of each member
    is a MemberEntry, which has a name and an optional submembers.
    """

    name: str
    members: DictMembers
    indentation: int
    force_alternative: bool

    def __init__(
        self,
        name: str,
        members: Optional[DictMembers] = None,
        indentation: int = 4,
        force_alternative: bool = False,
    ) -> None:
        if is_valid_name(name):
            self.name = name
        else:
            self.name = f"{name}_"
        self.members = members or {}
        self.indentation = indentation
        self.force_alternative = force_alternative

    def get_imports(self) -> Set[str]:
        imports = set()
        for sub_members in self.members.values():
            imports |= sub_members_to_imports(sub_members)
        return imports

    def update_members(self, members: DictMembers) -> None:
        if set(members.keys()) != self.keys:
            raise Exception("Keys don't match between members")

        for key, value in self.members.items():
            value |= members[key]

    def any_invalid_key(self) -> bool:
        return any(not is_valid_key(key) for key in self.keys)

    @property
    def keys(self) -> Set[str]:
        return set(self.members.keys())

    @property
    def depends_on(self) -> Set[str]:
        if not self.members:
            return set()
        members = set.union(*self.members.values())
        return set.union(*[m.depends_on for m in members], {m.name for m in members})

    def __hash__(self) -> int:
        return hash(str(";".join(self.keys)))

    def __eq__(self, other: Any) -> bool:
        """ DictEntries are equal if the keys are equal.

        The name and the values of each key don't matter, since the the name is
        just for the python type and the values are to know what type the keys
        can be, but the keys themselves are the only important thing
        """
        if self.__class__ != other.__class__:
            return False
        assert isinstance(other, self.__class__)

        return hash(self) == hash(other)

    def __repr__(self) -> str:
        return f"<DictEntry ({self.name})>"

    def __str__(self) -> str:
        out: List[str] = []

        if self.force_alternative or self.any_invalid_key():
            if not self.members:
                out.append(f'{self.name} = TypedDict("{self.name}", {{}}')
            else:
                out.append(f'{self.name} = TypedDict("{self.name}", {{')

                for key, value in self.members.items():
                    out.append(
                        f'{" " * self.indentation}"{key}": {sub_members_to_string(value)},'
                    )

                out.append("})")
        else:
            out.append(f"class {self.name}(TypedDict):")
            if not self.members:
                out.append(f'{" " * self.indentation}pass')
            else:
                for key, value in self.members.items():
                    out.append(
                        f"{' ' * self.indentation}{key}: {sub_members_to_string(value)}"
                    )

        return "\n".join(out)


@functools.total_ordering
class DependencyCmp:
    _name: str
    _depends_on: Set[str]

    def __init__(self, obj: EntryType) -> None:
        self._name = obj.name
        self._depends_on = obj.depends_on

    def __lt__(self, other: Any) -> bool:
        """ Considered less if other depends on it """
        if self.__class__ != other.__class__:
            raise TypeError(
                "DependencyCmp comparison only supports comparing to other instances of DependencyCmp"
            )
        assert isinstance(other, self.__class__)

        return self._name in other._depends_on

    def __eq__(self, other: Any) -> bool:
        """ Considered equal if other doesn't depend on it """
        if self.__class__ != other.__class__:
            raise TypeError(
                "DependencyCmp comparison only supports comparing to other instances of DependencyCmp"
            )
        assert isinstance(other, self.__class__)

        return self._name not in other._depends_on


def key_to_dependency_cmp(entry: Any) -> DependencyCmp:
    return DependencyCmp(entry)

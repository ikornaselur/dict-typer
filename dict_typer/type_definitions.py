from typing import Any, Dict, List, Optional, Set, Tuple, Type, Union

from dict_typer.models import (
    DictEntry,
    MemberEntry,
    key_to_dependency_cmp,
    sub_members_to_imports,
    sub_members_to_string,
)
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


Source = Union[str, int, float, bool, None, Dict, List]
NameMap = Dict[str, str]


class DefinitionBuilder:
    definitions: List[DictEntry]
    root_type_name: str
    type_postfix: str
    show_imports: bool
    source: Source
    name_map: NameMap

    _output: Optional[str] = None

    def __init__(
        self,
        source: Source,
        *,
        root_type_name: str = "Root",
        type_postfix: str = "",
        show_imports: bool = True,
        force_alternative: bool = False,
        name_map: NameMap = None,
    ) -> None:
        self.definitions = []

        self.root_type_name = root_type_name
        self.type_postfix = type_postfix
        self.show_imports = show_imports
        self.force_alternative = force_alternative
        if name_map:
            self.name_map = name_map
        else:
            self.name_map = {}

        self.source = source

    def _get_name(self, name: str) -> str:
        """ Return the mapped name if it exist """
        return self.name_map.get(name, name)

    def _add_definition(self, entry: DictEntry) -> DictEntry:
        """ Add an entry to the definions.

        If the entry is a DictEntry and there's an existing entry with the same
        keys, then combine the DictEntries
        """
        dicts_only = [d for d in self.definitions if isinstance(d, DictEntry)]
        for definition in dicts_only:
            if entry.keys == definition.keys:
                definition.update_members(entry.members)
                return definition
            if entry.name == definition.name:
                idx = 1
                new_name = f"{entry.name}{idx}"
                dicts_names = [d.name for d in dicts_only]
                while new_name in dicts_names:
                    idx += 1
                    new_name = f"{entry.name}{idx}"
                entry.name = new_name
        self.definitions.append(entry)
        return entry

    def _convert_list(self, key: str, lst: List, item_name: str) -> MemberEntry:
        entry = MemberEntry(key)

        idx = 0
        for item in lst:
            item_type = self._get_type(item, key=f"{item_name}{idx}")

            entry.sub_members.add(item_type)
            if isinstance(item_type, DictEntry):
                self._add_definition(item_type)
            idx += 1

        return entry

    def _convert_dict(self, type_name: str, dct: Dict) -> DictEntry:
        entry = DictEntry(
            self._get_name(type_name), force_alternative=self.force_alternative
        )
        for key, value in dct.items():
            value_type = self._get_type(value, key=key)
            if isinstance(value_type, DictEntry):
                definition = self._add_definition(value_type)
                value_type = definition
            entry.members[key] = {value_type}
        return entry

    def _get_type(self, item: Any, key: str) -> Union[MemberEntry, DictEntry]:
        if item is None:
            return MemberEntry("None")

        if isinstance(item, BASE_TYPES):
            return MemberEntry(type(item).__name__)

        if isinstance(item, (list, set, tuple, frozenset)):
            if isinstance(item, list):
                sequence_type_name = "List"
            elif isinstance(item, set):
                sequence_type_name = "Set"
            elif isinstance(item, frozenset):
                sequence_type_name = "FrozenSet"
            else:
                sequence_type_name = "Tuple"

            list_item_types: Set[Union[MemberEntry, DictEntry]] = set()
            idx = 0
            for value in item:
                item_type = self._get_type(value, key=f"{key}Item{idx}")
                if isinstance(item_type, DictEntry):
                    if item_type.members not in (
                        getattr(t, "members", None) for t in list_item_types
                    ):
                        list_item_types.add(item_type)
                        idx += 1
                        if isinstance(item_type, DictEntry):
                            self._add_definition(item_type)
                else:
                    list_item_types.add(item_type)

            return MemberEntry(sequence_type_name, sub_members=list_item_types)

        if isinstance(item, dict):
            return self._convert_dict(
                f"{key_to_class_name(key)}{self.type_postfix}", item
            )

        raise NotImplementedError(f"Type handling for '{type(item)}' not implemented")

    def build_output(self) -> str:
        if self._output:
            return self._output

        source_type = self._get_type(self.source, key=self.root_type_name)
        if isinstance(source_type, DictEntry):
            self._add_definition(source_type)
            root_item = None
        else:
            root_item = source_type

        # Convert the definitions to structured output
        self._output = ""

        if self.show_imports:
            typing_imports = set()
            typed_dict_import = False

            for definition in self.definitions:
                if isinstance(definition, DictEntry):
                    typed_dict_import = True
                typing_imports |= definition.get_imports()
            if root_item:
                typing_imports |= sub_members_to_imports({root_item})

            if typing_imports:
                self._output += "\n".join(
                    [f"from typing import {', '.join(sorted(typing_imports))}", "", ""]
                )
            if typed_dict_import:
                self._output += "\n".join(
                    ["from typing_extensions import TypedDict", "", "", ""]
                )

        self._output += "\n\n\n".join(
            [str(d) for d in sorted(self.definitions, key=key_to_dependency_cmp)]
        )

        if not isinstance(source_type, DictEntry):
            if len(self._output):
                self._output += "\n"
                if len(self.definitions):
                    self._output += "\n\n"
            self._output += f"{self.root_type_name}{self.type_postfix} = {sub_members_to_string({source_type})}"

        return self._output


def get_type_definitions(
    source: Source,
    root_type_name: str = "Root",
    type_postfix: str = "",
    show_imports: bool = True,
    force_alternative: bool = False,
    name_map: NameMap = None,
) -> str:
    builder = DefinitionBuilder(
        source,
        root_type_name=root_type_name,
        type_postfix=type_postfix,
        show_imports=show_imports,
        force_alternative=force_alternative,
        name_map=name_map,
    )

    return builder.build_output()

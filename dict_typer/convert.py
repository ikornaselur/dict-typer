from typing import Any, Dict, List, Optional, Set, Tuple, Type, Union

from dict_typer.exceptions import ConvertException
from dict_typer.models import (
    DictEntry,
    EntryType,
    MemberEntry,
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


def convert(
    source: Union[Dict, List],
    root_type_name: str = "Root",
    type_postfix: str = "Type",
    show_imports: bool = True,
) -> str:
    if not isinstance(source, (list, dict)):
        raise ConvertException(f"Unsupported source type: {type(source)}")

    source = source.copy()  # Copy the source as it will be modified

    definitions: List[DictEntry] = []
    root_list: Set[MemberEntry] = set()

    def add_definition(entry: EntryType) -> EntryType:
        """ Add an entry to the definions

        If the entry is a DictEntry and there's an existing entry with the same
        keys, then combine the DictEntries
        """
        if isinstance(entry, MemberEntry):
            root_list.add(entry)
            return entry
        else:
            for definition in [d for d in definitions if isinstance(d, DictEntry)]:
                if entry.keys == definition.keys:
                    definition.update_members(entry.members)
                    return definition
            else:
                definitions.append(entry)
                return entry

    def convert_list(key: str, l: List, item_name: str) -> MemberEntry:
        entry = MemberEntry(key)

        idx = 0
        for item in l:
            item_type = get_type(item, key=f"{item_name}{idx}")

            entry.sub_members.add(item_type)
            if isinstance(item_type, DictEntry):
                add_definition(item_type)
            idx += 1

        return entry

    def convert_dict(type_name: str, d: Dict) -> DictEntry:
        entry = DictEntry(type_name)
        for key, value in d.items():
            value_type = get_type(value, key=key)
            if isinstance(value_type, DictEntry):
                definition = add_definition(value_type)
                value_type = definition
            entry.members[key] = {value_type}

        return entry

    def get_type(item: Any, key: str) -> Union[MemberEntry, DictEntry]:
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
                item_type = get_type(value, key=f"{key}Item{idx}")
                if isinstance(item_type, DictEntry):
                    if item_type.members not in (
                        getattr(t, "members", None) for t in list_item_types
                    ):
                        list_item_types.add(item_type)
                        idx += 1
                        if isinstance(item_type, DictEntry):
                            add_definition(item_type)
                else:
                    list_item_types.add(item_type)

            return MemberEntry(sequence_type_name, sub_members=list_item_types)

        if isinstance(item, dict):
            return convert_dict(f"{key_to_class_name(key)}{type_postfix}", item)

        raise NotImplementedError(f"Type handling for '{type(item)}' not implemented")

    if isinstance(source, dict):
        add_definition(convert_dict(f"{root_type_name}{type_postfix}", source))
    else:
        add_definition(convert_list(f"List", source, item_name=f"{root_type_name}Item"))

    output = ""

    if show_imports:
        typing_imports = set()
        typed_dict_import = False

        for definition in definitions:
            if isinstance(definition, DictEntry):
                typed_dict_import = True
            typing_imports |= definition.get_imports()
        if root_list:
            typing_imports.add("List")
            typing_imports |= sub_members_to_imports(root_list)

        if typing_imports:
            output += "\n".join(
                [f"from typing import {', '.join(sorted(typing_imports))}", "", ""]
            )
        if typed_dict_import:
            output += "\n".join(["from typing_extensions import TypedDict", "", "", ""])

    output += "\n\n\n".join([str(d) for d in definitions])

    if root_list:
        if len(output):
            output += "\n"
            if len(definitions):
                output += "\n\n"
        output += f"{root_type_name}{type_postfix} = {sub_members_to_string(root_list)}"

    return output

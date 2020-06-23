import re
from keyword import iskeyword
from typing import TYPE_CHECKING, Dict, List, Set

if TYPE_CHECKING:
    from dict_typer.models import EntryType


def is_valid_key(key: str) -> bool:
    if iskeyword(key):
        return False
    return key.isidentifier()


def key_to_class_name(key: str) -> str:
    # First split on non characters
    parts1 = re.split(r"[^a-zA-Z0-9]", key)

    # Then split each if camelcase
    parts2: List[str] = []
    for part in parts1:
        if part.islower():
            parts2.append(part)
            continue

        # Assume it's pascal or camel case
        for sub_part in re.split(r"([A-Z][^A-Z]+)", part):
            if len(sub_part):
                parts2.append(sub_part)

    return "".join([part[0].upper() + part[1:].lower() for part in parts2 if part])


def get_imports(entry: "EntryType") -> Set[str]:
    """ Collect imports from the entry and all children """
    imports = set()

    to_process = {entry}
    processed = set()

    while len(to_process):
        item = to_process.pop()
        if item in processed:
            continue

        imports |= item.imports

        for sub_entry in item.sub_entries:
            if sub_entry not in processed:
                to_process.add(sub_entry)

        processed.add(item)

    return imports

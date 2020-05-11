import re
from keyword import iskeyword
from typing import List


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

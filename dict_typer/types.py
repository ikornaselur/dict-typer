from typing import Any, Tuple, Type

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


TYPING_MAPPING = {
    "list": "List",
    "tuple": "Tuple",
    "set": "Set",
    "frozenset": "FrozenSet",
    "dict": "Dict",
}


def get_type(item: Any) -> str:
    type_name = type(item).__name__

    if type_name in TYPING_MAPPING:
        return TYPING_MAPPING[type_name]

    if isinstance(item, BASE_TYPES):
        return type_name

    raise NotImplementedError(f"Typing not implemented for '{type(item)}'")

from typing import List, Union

from typing_extensions import TypedDict


class NestedDict(TypedDict):
    number: int
    string: str


class Level2(TypedDict):
    level3: NestedDict


class MultipeLevels(TypedDict):
    level2: Level2


NestedInvalid = TypedDict("NestedInvalid", {"numeric-id": int, "from": str})


class Root(TypedDict):
    number_int: int
    number_float: float
    string: str
    list_single_type: List[str]
    list_mixed_type: List[Union[float, int, str]]
    nested_dict: NestedDict
    same_nested_dict: NestedDict
    multipe_levels: MultipeLevels
    nested_invalid: NestedInvalid
    optional_items: List[Union[None, int, str]]

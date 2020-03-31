from dict_typer import convert


def test_convert_root_list_single_item() -> None:
    source = [{"id": 123}]

    # fmt: off
    expected = "\n".join([
        "from typing import List",
        "",
        "from typing_extensions import TypedDict",
        "",
        "",
        "class RootItemType(TypedDict):",
        "    id: int",
        "",
        "RootType = List[RootItemType]",
    ])
    # fmt: on

    assert convert(source) == expected


def test_convert_root_list_multiple_items() -> None:
    source = [
        {"id": 123},
        {"id": 456},
        {"id": 789},
    ]

    # fmt: off
    expected = "\n".join([
        "from typing import List",
        "",
        "from typing_extensions import TypedDict",
        "",
        "",
        "class RootItemType(TypedDict):",
        "    id: int",
        "",
        "RootType = List[RootItemType]",
    ])
    # fmt: on

    assert convert(source) == expected


def test_convert_root_list_multiple_mixed_items() -> None:
    source = [
        {"id": 123},
        {"value": "string"},
        {"id": 456},
        {"value": "strong"},
    ]

    # fmt: off
    expected = "\n".join([
        "from typing import List, Union",
        "",
        "from typing_extensions import TypedDict",
        "",
        "",
        "class RootItemType(TypedDict):",
        "    id: int",
        "",
        "class RootItemType1(TypedDict):",
        "    value: str",
        "",
        "RootType = List[Union[RootItemType, RootItemType1]]",
    ])
    # fmt: on

    assert convert(source) == expected


def test_convert_root_list_mixed_non_dict() -> None:
    source = [1, 2.0, "3"]

    # fmt: off
    expected = "\n".join([
        "from typing import List, Union",
        "",
        "",
        "RootType = List[Union[float, int, str]]",
    ])
    # fmt: on

    assert convert(source) == expected

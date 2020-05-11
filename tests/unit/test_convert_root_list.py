from dict_typer import get_type_definitions


def test_convert_root_list_single_item() -> None:
    source = [{"id": 123}]

    # fmt: off
    expected = "\n".join([
        "from typing import List",
        "",
        "from typing_extensions import TypedDict",
        "",
        "",
        "class RootItem0(TypedDict):",
        "    id: int",
        "",
        "",
        "Root = List[RootItem0]",
    ])
    # fmt: on

    assert expected == get_type_definitions(source)


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
        "class RootItem0(TypedDict):",
        "    id: int",
        "",
        "",
        "Root = List[RootItem0]",
    ])
    # fmt: on

    assert expected == get_type_definitions(source)


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
        "class RootItem0(TypedDict):",
        "    id: int",
        "",
        "",
        "class RootItem1(TypedDict):",
        "    value: str",
        "",
        "",
        "Root = List[Union[RootItem0, RootItem1]]",
    ])
    # fmt: on

    assert expected == get_type_definitions(source)


def test_convert_root_list_mixed_non_dict() -> None:
    source = [1, 2.0, "3"]

    # fmt: off
    expected = "\n".join([
        "from typing import List, Union",
        "",
        "",
        "Root = List[Union[float, int, str]]",
    ])
    # fmt: on

    assert expected == get_type_definitions(source)

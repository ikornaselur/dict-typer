from typing import List

from dict_typer import get_type_definitions


def test_convert_with_empty_list() -> None:
    source = {"items": []}  # type: ignore

    # fmt: off
    expected = "\n".join([
        "from typing import List",
        "",
        "from typing_extensions import TypedDict",
        "",
        "",
        "class Root(TypedDict):",
        "    items: List",
    ])
    # fmt: on

    assert expected == get_type_definitions(source)


def test_convert_empty_root_list() -> None:
    source: List = []

    # fmt: off
    expected = "\n".join([
        "from typing import List",
        "",
        "",
        "Root = List",
    ])
    # fmt: on

    assert expected == get_type_definitions(source)


def test_convert_with_simple_list() -> None:
    source = {"items": [1, 2, 3]}

    # fmt: off
    expected = "\n".join([
        "from typing import List",
        "",
        "from typing_extensions import TypedDict",
        "",
        "",
        "class Root(TypedDict):",
        "    items: List[int]",
    ])
    # fmt: on

    assert expected == get_type_definitions(source)


def test_convert_with_mixed_list() -> None:
    source = {"items": [1, "2", 3.5]}

    # fmt: off
    expected = "\n".join([
        "from typing import List, Union",
        "",
        "from typing_extensions import TypedDict",
        "",
        "",
        "class Root(TypedDict):",
        "    items: List[Union[float, int, str]]",
    ])
    # fmt: on

    assert expected == get_type_definitions(source)

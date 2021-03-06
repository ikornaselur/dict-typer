from dict_typer import get_type_definitions


def test_convert_with_empty_set() -> None:
    source = {"items": set()}  # type: ignore

    # fmt: off
    expected = "\n".join([
        "from typing import Set",
        "",
        "from typing_extensions import TypedDict",
        "",
        "",
        "class Root(TypedDict):",
        "    items: Set",
    ])
    # fmt: on

    assert expected == get_type_definitions(source)


def test_convert_with_simple_set() -> None:
    source = {"items": {1, 2, 3}}

    # fmt: off
    expected = "\n".join([
        "from typing import Set",
        "",
        "from typing_extensions import TypedDict",
        "",
        "",
        "class Root(TypedDict):",
        "    items: Set[int]",
    ])
    # fmt: on

    assert expected == get_type_definitions(source)


def test_convert_with_mixed_set() -> None:
    source = {"items": {1, "2", 3.5}}

    # fmt: off
    expected = "\n".join([
        "from typing import Set, Union",
        "",
        "from typing_extensions import TypedDict",
        "",
        "",
        "class Root(TypedDict):",
        "    items: Set[Union[float, int, str]]",
    ])
    # fmt: on

    assert expected == get_type_definitions(source)

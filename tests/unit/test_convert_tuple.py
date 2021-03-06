from dict_typer import get_type_definitions


def test_convert_with_empty_tuple() -> None:
    source = {"items": ()}  # type: ignore

    # fmt: off
    expected = "\n".join([
        "from typing import Tuple",
        "",
        "from typing_extensions import TypedDict",
        "",
        "",
        "class Root(TypedDict):",
        "    items: Tuple",
    ])
    # fmt: on

    assert expected == get_type_definitions(source)


def test_convert_with_simple_tuple() -> None:
    source = {"items": (1, 2, 3)}

    # fmt: off
    expected = "\n".join([
        "from typing import Tuple",
        "",
        "from typing_extensions import TypedDict",
        "",
        "",
        "class Root(TypedDict):",
        "    items: Tuple[int]",
    ])
    # fmt: on

    assert expected == get_type_definitions(source)


def test_convert_with_mixed_tuple() -> None:
    source = {"items": (1, "2", 3.5)}

    # fmt: off
    expected = "\n".join([
        "from typing import Tuple, Union",
        "",
        "from typing_extensions import TypedDict",
        "",
        "",
        "class Root(TypedDict):",
        "    items: Tuple[Union[float, int, str]]",
    ])
    # fmt: on

    assert expected == get_type_definitions(source)

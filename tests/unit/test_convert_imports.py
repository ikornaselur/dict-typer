from dict_typer import get_type_definitions


def test_convert_hides_import_optionally() -> None:
    source = {
        "itemsList": [1, 2.0, "3"],
        "itemsTuple": (4, 5, 6),
        "itemsSet": {7, 8, 9.0},
    }

    # fmt: off
    expected = "\n".join([
        "class Root(TypedDict):",
        "    itemsList: List[Union[float, int, str]]",
        "    itemsTuple: Tuple[int]",
        "    itemsSet: Set[Union[float, int]]",
    ])
    # fmt: on

    assert get_type_definitions(source, show_imports=False) == expected


def test_convert_optionally_adds_imports_with_nested_defs() -> None:
    source = {"itemsList": [1, 2, 3], "nest": {"itemsTuple": ({4, 5.0}, 5, 6)}}

    # fmt: off
    expected = "\n".join([
        "from typing import List, Set, Tuple, Union",
        "",
        "from typing_extensions import TypedDict",
        "",
        "",
        "class Nest(TypedDict):",
        "    itemsTuple: Tuple[Union[Set[Union[float, int]], int]]",
        "",
        "",
        "class Root(TypedDict):",
        "    itemsList: List[int]",
        "    nest: Nest",
    ])
    # fmt: on

    assert get_type_definitions(source, show_imports=True) == expected


def test_convert_imports_with_no_typing_imports() -> None:
    source = {"id": 10, "value": "value"}

    # fmt: off
    expected = "\n".join([
        "from typing_extensions import TypedDict",
        "",
        "",
        "class Root(TypedDict):",
        "    id: int",
        "    value: str",
    ])
    # fmt: on

    assert get_type_definitions(source, show_imports=True) == expected


def test_convert_imports_with_no_typed_dict() -> None:
    source = [1, 2, 3]

    # fmt: off
    expected = "\n".join([
        "from typing import List",
        "",
        "",
        "Root = List[int]",
    ])
    # fmt: on

    assert get_type_definitions(source, show_imports=True) == expected

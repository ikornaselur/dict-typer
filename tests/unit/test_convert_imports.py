from dict_typer import convert


def test_convert_hides_import_optionally() -> None:
    source = {
        "itemsList": [1, 2.0, "3"],
        "itemsTuple": (4, 5, 6),
        "itemsSet": {7, 8, 9.0},
    }

    # fmt: off
    expected = "\n".join([
        "class RootType(TypedDict):",
        "    itemsList: List[Union[float, int, str]]",
        "    itemsTuple: Tuple[int]",
        "    itemsSet: Set[Union[float, int]]",
    ])
    # fmt: on

    assert convert(source, show_imports=False) == expected


def test_convert_optionally_adds_imports_with_nested_defs() -> None:
    source = {"itemsList": [1, 2, 3], "nest": {"itemsTuple": ({4, 5.0}, 5, 6)}}

    # fmt: off
    expected = "\n".join([
        "from typing import List, Set, Tuple, Union",
        "",
        "from typing_extensions import TypedDict",
        "",
        "",
        "class NestType(TypedDict):",
        "    itemsTuple: Tuple[Union[Set[Union[float, int]], int]]",
        "",
        "class RootType(TypedDict):",
        "    itemsList: List[int]",
        "    nest: NestType",
    ])
    # fmt: on

    assert convert(source, show_imports=True) == expected


def test_convert_imports_with_no_typing_imports() -> None:
    source = {"id": 10, "value": "value"}

    # fmt: off
    expected = "\n".join([
        "from typing_extensions import TypedDict",
        "",
        "",
        "class RootType(TypedDict):",
        "    id: int",
        "    value: str",
    ])
    # fmt: on

    assert convert(source, show_imports=True) == expected


def test_convert_imports_with_no_typed_dict() -> None:
    source = [1, 2, 3]

    # fmt: off
    expected = "\n".join([
        "from typing import List",
        "",
        "",
        "RootType = List[int]",
    ])
    # fmt: on

    assert convert(source, show_imports=True) == expected

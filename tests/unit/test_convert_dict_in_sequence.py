from dict_typer import convert


def test_convert_list_of_repeated_dicts() -> None:
    source = {"dictList": [{"id": 123}, {"id": 456}, {"id": 789}]}

    # fmt: off
    expected = "\n".join([
        "from typing import List",
        "",
        "from typing_extensions import TypedDict",
        "",
        "",
        "class DictListItem0Type(TypedDict):",
        "    id: int",
        "",
        "",
        "class RootType(TypedDict):",
        "    dictList: List[DictListItem0Type]",
    ])
    # fmt: on

    assert expected == convert(source)


def test_convert_list_of_mixed_dicts() -> None:
    source = {"dictList": [{"foo": 123}, {"bar": 456}, {"baz": 789}, {"baz": 000}]}

    # fmt: off
    expected = "\n".join([
        "from typing import List, Union",
        "",
        "from typing_extensions import TypedDict",
        "",
        "",
        "class DictListItem0Type(TypedDict):",
        "    foo: int",
        "",
        "",
        "class DictListItem1Type(TypedDict):",
        "    bar: int",
        "",
        "",
        "class DictListItem2Type(TypedDict):",
        "    baz: int",
        "",
        "",
        "class RootType(TypedDict):",
        "    dictList: List[Union[DictListItem0Type, DictListItem1Type, DictListItem2Type]]",
    ])
    # fmt: on

    assert expected == convert(source)


def test_convert_list_of_repeated_dicts_different_types_combined() -> None:
    source = {"dictList": [{"id": 123}, {"id": 456.0}, {"id": "789"}]}

    # fmt: off
    expected = "\n".join([
        "from typing import List, Union",
        "",
        "from typing_extensions import TypedDict",
        "",
        "",
        "class DictListItem0Type(TypedDict):",
        "    id: Union[float, int, str]",
        "",
        "",
        "class RootType(TypedDict):",
        "    dictList: List[DictListItem0Type]",
    ])
    # fmt: on

    assert expected == convert(source)

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
        "class DictListItemType(TypedDict):",
        "    id: int",
        "",
        "class RootType(TypedDict):",
        "    dictList: List[DictListItemType]",
    ])
    # fmt: on

    assert convert(source) == expected


def test_convert_list_of_mixed_dicts() -> None:
    source = {"dictList": [{"foo": 123}, {"bar": 456}, {"baz": 789}, {"baz": 000}]}

    # fmt: off
    expected = "\n".join([
        "from typing import List, Union",
        "",
        "from typing_extensions import TypedDict",
        "",
        "",
        "class DictListItemType(TypedDict):",
        "    foo: int",
        "",
        "class DictListItemType1(TypedDict):",
        "    bar: int",
        "",
        "class DictListItemType2(TypedDict):",
        "    baz: int",
        "",
        "class RootType(TypedDict):",
        "    dictList: List[Union[DictListItemType, DictListItemType1, DictListItemType2]]",
    ])
    # fmt: on

    assert convert(source) == expected

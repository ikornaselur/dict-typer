from dict_typer import get_type_definitions


def test_convert_list_of_repeated_dicts() -> None:
    source = {"dictList": [{"id": 123}, {"id": 456}, {"id": 789}]}

    # fmt: off
    expected = "\n".join([
        "from typing import List",
        "",
        "from typing_extensions import TypedDict",
        "",
        "",
        "class DictListItem0(TypedDict):",
        "    id: int",
        "",
        "",
        "class Root(TypedDict):",
        "    dictList: List[DictListItem0]",
    ])
    # fmt: on

    assert expected == get_type_definitions(source)


def test_convert_list_of_mixed_dicts() -> None:
    source = {"dictList": [{"foo": 123}, {"bar": 456}, {"baz": 789}, {"baz": 000}]}

    # fmt: off
    expected = "\n".join([
        "from typing import List, Union",
        "",
        "from typing_extensions import TypedDict",
        "",
        "",
        "class DictListItem0(TypedDict):",
        "    foo: int",
        "",
        "",
        "class DictListItem1(TypedDict):",
        "    bar: int",
        "",
        "",
        "class DictListItem2(TypedDict):",
        "    baz: int",
        "",
        "",
        "class Root(TypedDict):",
        "    dictList: List[Union[DictListItem0, DictListItem1, DictListItem2]]",
    ])
    # fmt: on

    assert expected == get_type_definitions(source)


def test_convert_list_of_repeated_dicts_different_types_combined() -> None:
    source = {"dictList": [{"id": 123}, {"id": 456.0}, {"id": "789"}]}

    # fmt: off
    expected = "\n".join([
        "from typing import List, Union",
        "",
        "from typing_extensions import TypedDict",
        "",
        "",
        "class DictListItem0(TypedDict):",
        "    id: Union[float, int, str]",
        "",
        "",
        "class Root(TypedDict):",
        "    dictList: List[DictListItem0]",
    ])
    # fmt: on

    assert expected == get_type_definitions(source)

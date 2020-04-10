from dict_typer import convert


def test_convert_single_optional_in_list() -> None:
    source = [1, 2, None, 3, 4, None, 5, 6]

    # fmt: off
    expected = "\n".join([
        "from typing import List, Optional",
        "",
        "",
        "RootType = List[Optional[int]]",
    ])
    # fmt: on

    assert convert(source) == expected


def test_convert_not_optional_if_multiple_types_with_none() -> None:
    source = [1, 2, None, 3.0, 4.0, None, 5, 6]

    # fmt: off
    expected = "\n".join([
        "from typing import List, Union",
        "",
        "",
        "RootType = List[Union[None, float, int]]",
    ])
    # fmt: on

    assert convert(source) == expected


def test_convert_optional_combined_dicts() -> None:
    source = [{"value": "foo"}, {"value": None}]

    # fmt: off
    expected = "\n".join([
        "from typing_extensions import TypedDict",
        "",
        "",
        "class RootTypeItem(TypedDict):"
        "    value: Optional[str]",
        ""
        "RootType = List[RootTypeItem]",
    ])
    # fmt: on

    assert convert(source) == expected

from dict_typer import get_type_definitions


def test_convert_single_optional_in_list() -> None:
    source = [1, 2, None, 3, 4, None, 5, 6]

    # fmt: off
    expected = "\n".join([
        "from typing import List, Optional",
        "",
        "",
        "Root = List[Optional[int]]",
    ])
    # fmt: on

    assert expected == get_type_definitions(source)


def test_convert_not_optional_if_multiple_types_with_none() -> None:
    source = [1, 2, None, 3.0, 4.0, None, 5, 6]

    # fmt: off
    expected = "\n".join([
        "from typing import List, Union",
        "",
        "",
        "Root = List[Union[None, float, int]]",
    ])
    # fmt: on

    assert expected == get_type_definitions(source)


def test_convert_optional_combined_dicts() -> None:
    source = {
        "owner": {"name": "foo", "age": 44},
        "coOwner": {"name": "bar", "age": None},
    }

    # fmt: off
    expected = "\n".join([
        "from typing import Optional",
        "",
        "from typing_extensions import TypedDict",
        "",
        "",
        "class Owner(TypedDict):",
        "    name: str",
        "    age: Optional[int]",
        "",
        "",
        "class Root(TypedDict):",
        "    owner: Owner",
        "    coOwner: Owner",
    ])
    # fmt: on

    assert expected == get_type_definitions(source)

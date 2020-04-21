import pytest

from dict_typer import convert


def test_convert_with_nested_dict() -> None:
    source = {"nest": {"foo": "bar"}}

    # fmt: off
    expected = "\n".join([
        "from typing_extensions import TypedDict",
        "",
        "",
        "class NestType(TypedDict):",
        "    foo: str",
        "",
        "",
        "class RootType(TypedDict):",
        "    nest: NestType",
    ])
    # fmt: on

    assert expected == convert(source)


def test_convert_with_multiple_levels_nested_dict() -> None:
    source = {"level1": {"level2": {"level3": {"level4": "foo"}}}}

    # fmt: off
    expected = "\n".join([
        "from typing_extensions import TypedDict",
        "",
        "",
        "class Level3Type(TypedDict):",
        "    level4: str",
        "",
        "",
        "class Level2Type(TypedDict):",
        "    level3: Level3Type",
        "",
        "",
        "class Level1Type(TypedDict):",
        "    level2: Level2Type",
        "",
        "",
        "class RootType(TypedDict):",
        "    level1: Level1Type",
    ])
    # fmt: on

    assert expected == convert(source)


def test_convert_with_multiple_nested_dict() -> None:
    source = {"nest": {"foo": "bar"}, "other_nest": {"baz": "qux"}}

    # fmt: off
    expected = "\n".join([
        "from typing_extensions import TypedDict",
        "",
        "",
        "class NestType(TypedDict):",
        "    foo: str",
        "",
        "",
        "class OtherNestType(TypedDict):",
        "    baz: str",
        "",
        "",
        "class RootType(TypedDict):",
        "    nest: NestType",
        "    other_nest: OtherNestType",
    ])
    # fmt: on

    assert expected == convert(source)


def test_convert_with_repeated_nested_dict() -> None:
    source = {
        "nest": {"foo": "bar"},
        "other_nest": {"foo": "qux"},
        "unique_nest": {"baz": "qux"},
    }

    # fmt: off
    expected = "\n".join([
        "from typing_extensions import TypedDict",
        "",
        "",
        "class NestType(TypedDict):",
        "    foo: str",
        "",
        "",
        "class UniqueNestType(TypedDict):",
        "    baz: str",
        "",
        "",
        "class RootType(TypedDict):",
        "    nest: NestType",
        "    other_nest: NestType",
        "    unique_nest: UniqueNestType",
    ])
    # fmt: on

    assert expected == convert(source)


@pytest.mark.skip(reason="Known issue for later fixing")
def test_convert_nested_overlapping_dict() -> None:
    source = {
        "items": [
            {"id": {"foo": "foo", "primary": "bar"}},
            {"id": {"foo": "baz", "secondary": "qux"}},
        ]
    }

    # fmt: off
    expected = "\n".join([
        "from typing import List, Union",
        "",
        "from typing_extensions import TypedDict",
        "",
        "",
        "class IdType0(TypedDict):",
        "    foo: str",
        "    primary: str",
        "",
        "",
        "class IdType1(TypedDict):",
        "    foo: str",
        "    secondary: str",
        "",
        "",
        "class ItemsItem0Type(TypedDict):",
        "    id: Union[IdType0, IdType1]",
        "",
        "",
        "class RootType(TypedDict):",
        "    items: List[ItemsItem0Type]",
    ])
    # fmt: on

    assert expected == convert(source)

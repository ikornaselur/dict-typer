from typing import Dict

from dict_typer import get_type_definitions


def test_convert_empty_root_dict() -> None:
    source: Dict = {}

    # fmt: off
    expected = "\n".join([
        "from typing_extensions import TypedDict",
        "",
        "",
        "class Root(TypedDict):",
        "    pass",
    ])
    # fmt: on

    assert expected == get_type_definitions(source)


def test_convert_with_nested_empty_dict() -> None:
    source: Dict = {"nest": {}}

    # fmt: off
    expected = "\n".join([
        "from typing_extensions import TypedDict",
        "",
        "",
        "class Nest(TypedDict):",
        "    pass",
        "",
        "",
        "class Root(TypedDict):",
        "    nest: Nest",
    ])
    # fmt: on

    assert expected == get_type_definitions(source)


def test_convert_with_nested_dict() -> None:
    source = {"nest": {"foo": "bar"}}

    # fmt: off
    expected = "\n".join([
        "from typing_extensions import TypedDict",
        "",
        "",
        "class Nest(TypedDict):",
        "    foo: str",
        "",
        "",
        "class Root(TypedDict):",
        "    nest: Nest",
    ])
    # fmt: on

    assert expected == get_type_definitions(source)


def test_convert_with_multiple_levels_nested_dict() -> None:
    source = {"level1": {"level2": {"level3": {"level4": "foo"}}}}

    # fmt: off
    expected = "\n".join([
        "from typing_extensions import TypedDict",
        "",
        "",
        "class Level3(TypedDict):",
        "    level4: str",
        "",
        "",
        "class Level2(TypedDict):",
        "    level3: Level3",
        "",
        "",
        "class Level1(TypedDict):",
        "    level2: Level2",
        "",
        "",
        "class Root(TypedDict):",
        "    level1: Level1",
    ])
    # fmt: on

    assert expected == get_type_definitions(source)


def test_convert_with_multiple_nested_dict() -> None:
    source = {"nest": {"foo": "bar"}, "other_nest": {"baz": "qux"}}

    # fmt: off
    expected = "\n".join([
        "from typing_extensions import TypedDict",
        "",
        "",
        "class Nest(TypedDict):",
        "    foo: str",
        "",
        "",
        "class OtherNest(TypedDict):",
        "    baz: str",
        "",
        "",
        "class Root(TypedDict):",
        "    nest: Nest",
        "    other_nest: OtherNest",
    ])
    # fmt: on

    assert expected == get_type_definitions(source)


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
        "class Nest(TypedDict):",
        "    foo: str",
        "",
        "",
        "class UniqueNest(TypedDict):",
        "    baz: str",
        "",
        "",
        "class Root(TypedDict):",
        "    nest: Nest",
        "    other_nest: Nest",
        "    unique_nest: UniqueNest",
    ])
    # fmt: on

    assert expected == get_type_definitions(source)


def test_convert_nested_overlapping_dict() -> None:
    source = [
        {"x": {"foo": "bar"}},
        {"x": {"baz": "qux"}},
    ]

    # fmt: off
    expected = "\n".join([
        "from typing import List, Union",
        "",
        "from typing_extensions import TypedDict",
        "",
        "",
        "class X(TypedDict):",
        "    foo: str",
        "",
        "",
        "class X1(TypedDict):",
        "    baz: str",
        "",
        "",
        "class RootItem0(TypedDict):",
        "    x: Union[X, X1]",
        "",
        "",
        "Root = List[RootItem0]",
    ])
    # fmt: on

    assert expected == get_type_definitions(source)


def test_convert_nested_same_keys() -> None:
    source = {"foo": {"foo": 10}}

    # fmt: off
    expected = "\n".join([
        "from typing import Union",
        "",
        "from typing_extensions import TypedDict",
        "",
        "",
        "class Foo(TypedDict):",
        "    foo: Union[Foo, int]",
    ])
    # fmt: on

    assert expected == get_type_definitions(source)


def test_convert_nested_same_keys_further_down() -> None:
    source = {"foo": {"bar": {"foo": 10}}}

    expected = "\n".join(
        [
            "from typing import Union",
            "",
            "from typing_extensions import TypedDict",
            "",
            "",
            "class Foo(TypedDict):",
            "    bar: Bar",
            "",
            "",
            "class Bar(TypedDict):",
            "    foo: Union[Foo, int]",
        ]
    )

    assert expected == get_type_definitions(source)


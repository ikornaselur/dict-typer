from dict_typer import convert


def test_convert_simple_json() -> None:
    source = {"id": 123, "item": "value", "progress": 0.71}

    # fmt: off
    expected = "\n".join([
        "class RootType(TypedDict):",
        "    id: int",
        "    item: str",
        "    progress: float",
    ])
    # fmt: on

    assert convert(source) == expected


def test_convert_builtins() -> None:
    source = {
        "str_type": "str",
        "bytes_type": b"bytes",
        "int_type": 1,
        "float_type": 1.5,
        "complex_type": 1 + 1j,
    }

    # fmt: off
    expected = "\n".join([
        "class RootType(TypedDict):",
        "    str_type: str",
        "    bytes_type: bytes",
        "    int_type: int",
        "    float_type: float",
        "    complex_type: complex",
    ])
    # fmt: on

    assert convert(source) == expected


def test_convert_with_empty_list() -> None:
    source = {"items": []}  # type: ignore

    # fmt: off
    expected = "\n".join([
        "class RootType(TypedDict):",
        "    items: List",
    ])
    # fmt: on

    assert convert(source) == expected


def test_convert_with_simple_list() -> None:
    source = {"items": [1, 2, 3]}

    # fmt: off
    expected = "\n".join([
        "class RootType(TypedDict):",
        "    items: List[int]",
    ])
    # fmt: on

    assert convert(source) == expected


def test_convert_with_mixed_list() -> None:
    source = {"items": [1, "2", 3.5]}

    # fmt: off
    expected = "\n".join([
        "class RootType(TypedDict):",
        "    items: List[Union[float, int, str]]",
    ])
    # fmt: on

    assert convert(source) == expected


def test_convert_with_empty_tuple() -> None:
    source = {"items": ()}  # type: ignore

    # fmt: off
    expected = "\n".join([
        "class RootType(TypedDict):",
        "    items: Tuple",
    ])
    # fmt: on

    assert convert(source) == expected


def test_convert_with_simple_tuple() -> None:
    source = {"items": (1, 2, 3)}

    # fmt: off
    expected = "\n".join([
        "class RootType(TypedDict):",
        "    items: Tuple[int]",
    ])
    # fmt: on

    assert convert(source) == expected


def test_convert_with_mixed_tuple() -> None:
    source = {"items": (1, "2", 3.5)}

    # fmt: off
    expected = "\n".join([
        "class RootType(TypedDict):",
        "    items: Tuple[Union[float, int, str]]",
    ])
    # fmt: on

    assert convert(source) == expected


def test_convert_with_nested_dict() -> None:
    source = {"nest": {"foo": "bar"}}

    # fmt: off
    expected = "\n".join([
        "class RootType(TypedDict):",
        "    nest: NestType",
        "",
        "class NestType(TypedDict):",
        "    foo: str",
    ])
    # fmt: on

    assert convert(source) == expected


def test_convert_with_multiple_nested_dict() -> None:
    source = {"nest": {"foo": "bar"}, "other_nest": {"baz": "qux"}}

    # fmt: off
    expected = "\n".join([
        "class RootType(TypedDict):",
        "    nest: NestType",
        "    other_nest: OtherNestType",
        "",
        "class NestType(TypedDict):",
        "    foo: str",
        "",
        "class OtherNestType(TypedDict):",
        "    baz: str",
    ])
    # fmt: on

    assert convert(source) == expected


def test_convert_with_repeated_nested_dict() -> None:
    source = {
        "nest": {"foo": "bar"},
        "other_nest": {"foo": "qux"},
        "unique_nest": {"baz": "qux"},
    }

    # fmt: off
    expected = "\n".join([
        "class RootType(TypedDict):",
        "    nest: NestType",
        "    other_nest: NestType",
        "    unique_nest: UniqueNestType",
        "",
        "class NestType(TypedDict):",
        "    foo: str",
        "",
        "class UniqueNestType(TypedDict):",
        "    baz: str",
    ])
    # fmt: on

    assert convert(source) == expected


def test_convert_optionally_adds_imports() -> None:
    source = {"itemsList": [1, 2.0, "3"], "itemsTuple": (4, 5, 6)}

    # fmt: off
    expected = "\n".join([
        "from typing import List, Tuple, Union",
        "",
        "from typing_extensions import TypedDict",
        "",
        "",
        "class RootType(TypedDict):",
        "    itemsList: List[Union[float, int, str]]",
        "    itemsTuple: Tuple[int]",
    ])
    # fmt: on

    assert convert(source, show_imports=True) == expected


def test_convert_optionally_adds_imports_with_nested_defs() -> None:
    source = {"itemsList": [1, 2, 3], "nest": {"itemsTuple": (4, 5, 6)}}

    # fmt: off
    expected = "\n".join([
        "from typing import List, Tuple",
        "",
        "from typing_extensions import TypedDict",
        "",
        "",
        "class RootType(TypedDict):",
        "    itemsList: List[int]",
        "    nest: NestType",
        "",
        "class NestType(TypedDict):",
        "    itemsTuple: Tuple[int]",
    ])
    # fmt: on

    assert convert(source, show_imports=True) == expected

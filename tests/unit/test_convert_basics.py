from dict_typer import get_type_definitions


def test_convert_simple_json() -> None:
    source = {"id": 123, "item": "value", "progress": 0.71}

    # fmt: off
    expected = "\n".join([
        "from typing_extensions import TypedDict",
        "",
        "",
        "class Root(TypedDict):",
        "    id: int",
        "    item: str",
        "    progress: float",
    ])
    # fmt: on

    assert expected == get_type_definitions(source)


def test_convert_base_types() -> None:
    source = {
        "bool_type": True,
        "bytearray_type": bytearray([102, 111, 111]),
        "bytes_types": b"foo",
        "complex_Type": 1 + 1j,
        "enumerate_type": enumerate(["a", "b", "c"]),
        "float_type": 1.2,
        "int_type": 1,
        "memoryview_type": memoryview(b"foo"),
        "range_type": range(30),
        "str_type": "foo",
        "filter_type": filter(lambda x: x < 10, range(20)),
        "map_type": map(lambda x: x * 2, range(20)),
        "zip_type": zip([1, 2], ["a", "b"]),
        "list_type": [1, 2, 3],
        "tuple_type": (1, 2, 3),
        "set_type": {1, 2, 3},
        "frozenset_type": frozenset([1, 2, 3]),
    }

    # fmt: off
    expected = "\n".join([
        "from typing import FrozenSet, List, Set, Tuple",
        "",
        "from typing_extensions import TypedDict",
        "",
        "",
        "class Root(TypedDict):",
        "    bool_type: bool",
        "    bytearray_type: bytearray",
        "    bytes_types: bytes",
        "    complex_Type: complex",
        "    enumerate_type: enumerate",
        "    float_type: float",
        "    int_type: int",
        "    memoryview_type: memoryview",
        "    range_type: range",
        "    str_type: str",
        "    filter_type: filter",
        "    map_type: map",
        "    zip_type: zip",
        "    list_type: List[int]",
        "    tuple_type: Tuple[int]",
        "    set_type: Set[int]",
        "    frozenset_type: FrozenSet[int]",
    ])
    # fmt: on

    assert expected == get_type_definitions(source)


def test_convert_none() -> None:
    source = {"value": None}

    # fmt: off
    expected = "\n".join([
        "from typing_extensions import TypedDict",
        "",
        "",
        "class Root(TypedDict):",
        "    value: None",
    ])
    # fmt: on

    assert expected == get_type_definitions(source)

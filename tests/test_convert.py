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


"""
def test_convert_with_nested_dict() -> None:
    source = {"nest": {"foo": "bar"}}

    # fmt: off
    expected = "\n".join([
        "class RootType(TypedDict):",
        "    nest: NestType",
        "",
        "class NextType(TypedDict):",
        "    foo: str",
    ])
    # fmt: on

    assert convert(source) == expected
"""

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


def test_convert_none() -> None:
    source = {"value": None}

    # fmt: off
    expected = "\n".join([
        "class RootType(TypedDict):",
        "    value: None",
    ])
    # fmt: on

    assert convert(source) == expected


def test_convert_list_with_none_as_optional() -> None:
    source = {"items": [1, 2, None, 3], "mixedItems": [1, "2", None, "4", 5]}

    # fmt: off
    expected = "\n".join([
        "class RootType(TypedDict):",
        "    items: List[Union[None, int]]",
        "    mixedItems: List[Union[None, int, str]]",
    ])
    # fmt: on

    assert convert(source) == expected

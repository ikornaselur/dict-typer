import json

from dict_typer import convert


def test_convert_simple_json() -> None:
    source = json.dumps({"id": 123, "item": "value", "progress": 0.71})

    # fmt: off
    expected = "\n".join([
        "class RootType(TypedDict):",
        "    id: int",
        "    item: str",
        "    progress: float",
    ])
    # fmt: on

    assert convert(source) == expected


def test_convert_with_empty_list() -> None:
    source = json.dumps({"items": []})

    # fmt: off
    expected = "\n".join([
        "class RootType(TypedDict):",
        "    items: List",
    ])
    # fmt: on

    assert convert(source) == expected


def test_convert_with_simple_list() -> None:
    source = json.dumps({"items": [1, 2, 3]})

    # fmt: off
    expected = "\n".join([
        "class RootType(TypedDict):",
        "    items: List[int]",
    ])
    # fmt: on

    assert convert(source) == expected


def test_convert_with_mixed_list() -> None:
    source = json.dumps({"items": [1, "2", 3.5]})

    # fmt: off
    expected = "\n".join([
        "class RootType(TypedDict):",
        "    items: List[Union[float, int, str]]",
    ])
    # fmt: on

    assert convert(source) == expected

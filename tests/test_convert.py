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

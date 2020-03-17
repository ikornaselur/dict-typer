import json

from dict_typer import convert


def test_convert_simple_json() -> None:
    source = json.dumps({"id": "123"})

    # fmt: off
    expected = "\n".join([
        "class RootType(TypedDict):",
        "    id: str",
    ])
    # fmt: on

    assert convert(source) == expected

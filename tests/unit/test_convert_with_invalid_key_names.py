from dict_typer import get_type_definitions


def test_convert_with_invalid_key_names() -> None:
    source = {"invalid-key": 123, "from": "far away"}

    # fmt: off
    expected = "\n".join([
        "from typing_extensions import TypedDict",
        "",
        "",
        'Root = TypedDict("Root", {',
        '    "invalid-key": int,',
        '    "from": str,',
        '})'
    ])
    # fmt: on

    assert expected == get_type_definitions(source)


def test_convert_with_invalid_key_names_nested() -> None:
    source = {"invalid-key": {"id": 123}}

    # fmt: off
    expected = "\n".join([
        "from typing_extensions import TypedDict",
        "",
        "",
        "class InvalidKey(TypedDict):",
        "    id: int",
        "",
        "",
        'Root = TypedDict("Root", {',
        '    "invalid-key": InvalidKey,',
        '})'
    ])
    # fmt: on

    assert expected == get_type_definitions(source)

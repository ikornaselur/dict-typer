from dict_typer import convert


def test_convert_with_invalid_key_names() -> None:
    source = {"invalid-key": 123, "from": "far away"}

    # fmt: off
    expected = "\n".join([
        'RootType = TypedDict("RootType", {',
        '    "invalid-key": int,',
        '    "from": str,',
        '})'
    ])
    # fmt: on

    assert convert(source) == expected


def test_convert_with_invalid_key_names_nested() -> None:
    source = {"invalid-key": {"id": 123}}

    # fmt: off
    expected = "\n".join([
        "class InvalidKeyType(TypedDict):",
        "    id: int",
        "",
        'RootType = TypedDict("RootType", {',
        '    "invalid-key": InvalidKeyType,',
        '})'
    ])
    # fmt: on

    assert convert(source) == expected

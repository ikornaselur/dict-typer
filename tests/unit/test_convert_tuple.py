from dict_typer import convert


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

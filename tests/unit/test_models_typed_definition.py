from dict_typer.models import TypedDefinion


def test_typed_definition_printable_primary() -> None:
    td = TypedDefinion(name="TestType", members=[("foo", "str")])

    # fmt: off
    expected = "\n".join([
        "class TestType(TypedDict):",
        "    foo: str",
    ])
    # fmt: on

    assert td.printable(replacements={}, alternative=False) == expected


def test_typed_definition_printable_alternative() -> None:
    td = TypedDefinion(name="TestType", members=[("foo", "str")])

    # fmt: off
    expected = "\n".join([
        'TestType = TypedDict("TestType", {',
        '    "foo": str',
        '})'
    ])
    # fmt: on

    assert td.printable(replacements={}, alternative=True) == expected


def test_typed_definition_printable_forces_alternative_if_invalid() -> None:
    td = TypedDefinion(name="TestType", members=[("foo-bar", "str")])

    # fmt: off
    expected = "\n".join([
        'TestType = TypedDict("TestType", {',
        '    "foo-bar": str',
        '})'
    ])
    # fmt: on

    assert td.printable(replacements={}, alternative=False) == expected

from dict_typer.models import MemberDefinition, TypedDefinion


def test_typed_definition_printable_primary() -> None:
    td = TypedDefinion(
        name="TestType",
        members=[
            MemberDefinition(name="foo", types=["str"]),
            MemberDefinition(name="bar", types=["int"]),
        ],
    )

    # fmt: off
    expected = "\n".join([
        "class TestType(TypedDict):",
        "    foo: str",
        "    bar: int",
    ])
    # fmt: on

    assert td.printable(replacements={}, alternative=False) == expected


def test_typed_definition_printable_alternative() -> None:
    td = TypedDefinion(
        name="TestType",
        members=[
            MemberDefinition(name="foo", types=["str"]),
            MemberDefinition(name="bar", types=["int"]),
        ],
    )

    # fmt: off
    expected = "\n".join([
        'TestType = TypedDict("TestType", {',
        '    "foo": str,',
        '    "bar": int,',
        '})'
    ])
    # fmt: on

    assert td.printable(replacements={}, alternative=True) == expected


def test_typed_definition_printable_forces_alternative_if_invalid() -> None:
    td = TypedDefinion(
        name="TestType",
        members=[
            MemberDefinition(name="foo-bar", types=["str"]),
            MemberDefinition(name="baz-qux", types=["int"]),
        ],
    )

    # fmt: off
    expected = "\n".join([
        'TestType = TypedDict("TestType", {',
        '    "foo-bar": str,',
        '    "baz-qux": int,',
        '})'
    ])
    # fmt: on

    assert td.printable(replacements={}, alternative=False) == expected

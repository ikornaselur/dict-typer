from dict_typer import get_type_definitions


def test_convert_with_a_name_map() -> None:
    source = {"id": 123, "item": "value", "things": [{"foo": "bar"}, {"baz": "quz"}]}

    name_map = {
        "Root": "Source",
        "ThingsItem0": "Foo",
        "ThingsItem1": "Baz",
        "NotUser": "DoesntMatter",
    }

    expected = "\n".join(
        [
            "from typing import List, Union",
            "",
            "from typing_extensions import TypedDict",
            "",
            "",
            "class Foo(TypedDict):",
            "    foo: str",
            "",
            "",
            "class Baz(TypedDict):",
            "    baz: str",
            "",
            "",
            "class Source(TypedDict):",
            "    id: int",
            "    item: str",
            "    things: List[Union[Baz, Foo]]",
        ]
    )

    assert expected == get_type_definitions(source, name_map=name_map)

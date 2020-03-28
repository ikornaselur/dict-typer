import json
from typing import Dict, List, Union

from dict_typer import convert


def fixture(name: str) -> Union[Dict, List]:
    with open(f"tests/integration/fixtures/{name}.json", "r") as f:
        return json.load(f)


def test_example1() -> None:
    source = fixture("example1")

    # fmt: off
    expected = "\n".join([
        "from typing import List",
        "",
        "from typing_extensions import TypedDict",
        "",
        "",
        "class GlossDefType(TypedDict):",
        "    para: str",
        "    GlossSeeAlso: List[str]",
        "",
        "class GlossEntryType(TypedDict):",
        "    ID: str",
        "    SortAs: str",
        "    GlossTerm: str",
        "    Acronym: str",
        "    Abbrev: str",
        "    GlossDef: GlossDefType",
        "    GlossSee: str",
        "",
        "class GlossListType(TypedDict):",
        "    GlossEntry: GlossEntryType",
        "",
        "class GlossDivType(TypedDict):",
        "    title: str",
        "    GlossList: GlossListType",
        "",
        "class GlossaryType(TypedDict):",
        "    title: str",
        "    GlossDiv: GlossDivType",
        "",
        "class RootType(TypedDict):",
        "    glossary: GlossaryType",
    ])
    # fmt: on

    assert convert(source, show_imports=True) == expected


def test_example2() -> None:
    source = fixture("example2")

    # fmt: off
    expected = "\n".join([
        "from typing import List",
        "",
        "from typing_extensions import TypedDict",
        "",
        "",
        "class MenuitemItemType(TypedDict):",
        "    value: str",
        "    onclick: str",
        "",
        "class PopupType(TypedDict):",
        "    menuitem: List[MenuitemItemType]",
        "",
        "class MenuType(TypedDict):",
        "    id: str",
        "    value: str",
        "    popup: PopupType",
        "",
        "class RootType(TypedDict):",
        "    menu: MenuType",
    ])
    # fmt: on

    assert convert(source, show_imports=True) == expected


def test_example3() -> None:
    source = fixture("example3")

    # fmt: off
    expected = "\n".join([
        "from typing_extensions import TypedDict",
        "",
        "",
        "class WindowType(TypedDict):",
        "    title: str",
        "    name: str",
        "    width: int",
        "    height: int",
        "",
        "class ImageType(TypedDict):",
        "    src: str",
        "    name: str",
        "    hOffset: int",
        "    vOffset: int",
        "    alignment: str",
        "",
        "class TextType(TypedDict):",
        "    data: str",
        "    size: int",
        "    style: str",
        "    name: str",
        "    hOffset: int",
        "    vOffset: int",
        "    alignment: str",
        "    onMouseUp: str",
        "",
        "class WidgetType(TypedDict):",
        "    debug: str",
        "    window: WindowType",
        "    image: ImageType",
        "    text: TextType",
        "",
        "class RootType(TypedDict):",
        "    widget: WidgetType",
    ])
    # fmt: on

    assert convert(source, show_imports=True) == expected


def test_example4() -> None:
    source = fixture("example4")

    # fmt: off
    expected = "\n".join([

    ])
    # fmt: on

    assert convert(source, show_imports=True) == expected

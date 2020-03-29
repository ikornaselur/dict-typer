import json
from typing import Dict, List, Union

from dict_typer import convert


def json_org_fixture(num: int) -> Union[Dict, List]:
    with open(f"tests/integration/fixtures/json.org.example{num}.json", "r") as f:
        return json.load(f)


def sitepoint_com_fixture(num: int) -> Union[Dict, List]:
    with open(f"tests/integration/fixtures/sitepoint.com.example{num}.json", "r") as f:
        return json.load(f)


def test_json_org_example1() -> None:
    source = json_org_fixture(1)

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


def test_json_org_example2() -> None:
    source = json_org_fixture(2)

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


def test_json_org_example3() -> None:
    source = json_org_fixture(3)

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


def test_json_org_example4() -> None:
    source = json_org_fixture(4)

    # fmt: off
    expected = "\n".join([
        'from typing import List, Union',
        '',
        'from typing_extensions import TypedDict',
        '',
        '',
        'InitParamType = TypedDict("InitParamType", {',
        '    "configGlossary:installationAt": str,',
        '    "configGlossary:adminEmail": str,',
        '    "configGlossary:poweredBy": str,',
        '    "configGlossary:poweredByIcon": str,',
        '    "configGlossary:staticPath": str,',
        '    "templateProcessorClass": str,',
        '    "templateLoaderClass": str,',
        '    "templatePath": str,',
        '    "templateOverridePath": str,',
        '    "defaultListTemplate": str,',
        '    "defaultFileTemplate": str,',
        '    "useJSP": bool,',
        '    "jspListTemplate": str,',
        '    "jspFileTemplate": str,',
        '    "cachePackageTagsTrack": int,',
        '    "cachePackageTagsStore": int,',
        '    "cachePackageTagsRefresh": int,',
        '    "cacheTemplatesTrack": int,',
        '    "cacheTemplatesStore": int,',
        '    "cacheTemplatesRefresh": int,',
        '    "cachePagesTrack": int,',
        '    "cachePagesStore": int,',
        '    "cachePagesRefresh": int,',
        '    "cachePagesDirtyRead": int,',
        '    "searchEngineListTemplate": str,',
        '    "searchEngineFileTemplate": str,',
        '    "searchEngineRobotsDb": str,',
        '    "useDataStore": bool,',
        '    "dataStoreClass": str,',
        '    "redirectionClass": str,',
        '    "dataStoreName": str,',
        '    "dataStoreDriver": str,',
        '    "dataStoreUrl": str,',
        '    "dataStoreUser": str,',
        '    "dataStorePassword": str,',
        '    "dataStoreTestQuery": str,',
        '    "dataStoreLogFile": str,',
        '    "dataStoreInitConns": int,',
        '    "dataStoreMaxConns": int,',
        '    "dataStoreConnUsageLimit": int,',
        '    "dataStoreLogLevel": str,',
        '    "maxUrlLength": int,',
        '})',
        '',
        'ServletItemType = TypedDict("ServletItemType", {',
        '    "servlet-name": str,',
        '    "servlet-class": str,',
        '    "init-param": InitParamType,',
        '})',
        '',
        'class InitParamType(TypedDict):',
        '    mailHost: str',
        '    mailHostOverride: str',
        '',
        'ServletItemType1 = TypedDict("ServletItemType1", {',
        '    "servlet-name": str,',
        '    "servlet-class": str,',
        '})',
        '',
        'class InitParamType(TypedDict):',
        '    templatePath: str',
        '    log: int',
        '    logLocation: str',
        '    logMaxSize: str',
        '    dataLog: int',
        '    dataLogLocation: str',
        '    dataLogMaxSize: str',
        '    removePageCache: str',
        '    removeTemplateCache: str',
        '    fileTransferFolder: str',
        '    lookInContext: int',
        '    adminGroupID: int',
        '    betaServer: bool',
        '',
        'class ServletMappingType(TypedDict):',
        '    cofaxCDS: str',
        '    cofaxEmail: str',
        '    cofaxAdmin: str',
        '    fileServlet: str',
        '    cofaxTools: str',
        '',
        'TaglibType = TypedDict("TaglibType", {',
        '    "taglib-uri": str,',
        '    "taglib-location": str,',
        '})',
        '',
        'WebAppType = TypedDict("WebAppType", {',
        '    "servlet": List[Union[ServletItemType, ServletItemType1]],',
        '    "servlet-mapping": ServletMappingType,',
        '    "taglib": TaglibType,',
        '})',
        '',
        'RootType = TypedDict("RootType", {',
        '    "web-app": WebAppType,',
        '})',
    ])
    # fmt: on

    assert convert(source, show_imports=True) == expected


def test_json_org_example5() -> None:
    source = json_org_fixture(5)

    # fmt: off
    expected = "\n".join([
        "from typing import List, Union",
        "",
        "from typing_extensions import TypedDict",
        "",
        "",
        "class ItemsItemType(TypedDict):",
        "    id: str",
        "",
        "class ItemsItemType1(TypedDict):",
        "    id: str",
        "    label: str",
        "",
        "class MenuType(TypedDict):",
        "    header: str",
        "    items: List[Union[ItemsItemType, ItemsItemType1, None]]",
        "",
        "class RootType(TypedDict):",
        "    menu: MenuType",
    ])
    # fmt: on

    assert convert(source, show_imports=True) == expected


def test_sitepoint_com_example1() -> None:
    source = sitepoint_com_fixture(1)

    # fmt: off
    expected = "\n".join([
        "from typing import List, Union",
        "",
        "from typing_extensions import TypedDict",
        "",
        "",
        "class CodeType(TypedDict):",
        "    rgba: List[int]",
        "    hex: str",
        "",
        "class ColorsItemType(TypedDict):",
        "    color: str",
        "    category: str",
        "    type: str",
        "    code: CodeType",
        "",
        "class ColorsItemType1(TypedDict):",
        "    color: str",
        "    category: str",
        "    code: CodeType",
        "",
        "class RootType(TypedDict):",
        "    colors: List[Union[ColorsItemType, ColorsItemType1]]",
    ])
    # fmt: on

    assert convert(source, show_imports=True) == expected


def test_sitepoint_com_example2() -> None:
    source = sitepoint_com_fixture(2)

    # fmt: off
    expected = "\n".join([
        "from typing import List, Union",
        "",
        "from typing_extensions import TypedDict",
        "",
        "",
        "class MarkersItemType(TypedDict):",
        "    name: str",
        "    position: List[float]",
        "",
        "class MarkersItemType1(TypedDict):",
        "    name: str",
        "    location: List[float]",
        "",
        "class RootType(TypedDict):",
        "    markers: List[Union[MarkersItemType, MarkersItemType1]]",
    ])
    # fmt: on

    assert convert(source, show_imports=True) == expected


def test_sitepoint_com_example3() -> None:
    source = sitepoint_com_fixture(3)

    # fmt: off
    expected = "\n".join([
        "from typing import List",
        "",
        "from typing_extensions import TypedDict",
        "",
        "",
        "class PageInfoType(TypedDict):",
        "    totalResults: int",
        "    resultsPerPage: int",
        "",
        "class IdType(TypedDict):",
        "    kind: str",
        "    channelId: str",
        "",
        "class ItemsItemType(TypedDict):",
        "    kind: str",
        "    etag: str",
        "    id: IdType",
        "",
        "class IdType(TypedDict):",
        "    kind: str",
        "    videoId: str",
        "",
        "class RootType(TypedDict):",
        "    kind: str",
        "    etag: str",
        "    nextPageToken: str",
        "    regionCode: str",
        "    pageInfo: PageInfoType",
        "    items: List[ItemsItemType]",
    ])
    # fmt: on

    assert convert(source, show_imports=True) == expected


def test_sitepoint_com_example4() -> None:
    source = sitepoint_com_fixture(4)

    # fmt: off
    expected = "\n".join([
        "from typing import List",
        "",
        "from typing_extensions import TypedDict",
        "",
        "",
        "class HashtagsItemType(TypedDict):",
        "    text: str",
        "    indices: List[int]",
        "",
        "class UrlsItemType(TypedDict):",
        "    url: str",
        "    expanded_url: str",
        "    display_url: str",
        "    indices: List[int]",
        "",
        "class EntitiesType(TypedDict):",
        "    hashtags: List[HashtagsItemType]",
        "    symbols: List",
        "    user_mentions: List",
        "    urls: List[UrlsItemType]",
        "",
        "class UrlType(TypedDict):",
        "    urls: List[UrlsItemType]",
        "",
        "class DescriptionType(TypedDict):",
        "    urls: List",
        "",
        "class EntitiesType(TypedDict):",
        "    url: UrlType",
        "    description: DescriptionType",
        "",
        "class UserType(TypedDict):",
        "    id: int",
        "    id_str: str",
        "    name: str",
        "    screen_name: str",
        "    location: str",
        "    description: str",
        "    url: str",
        "    entities: EntitiesType",
        "    protected: bool",
        "    followers_count: int",
        "    friends_count: int",
        "    listed_count: int",
        "    created_at: str",
        "    favourites_count: int",
        "    utc_offset: int",
        "    time_zone: str",
        "",
        "class RootItemType(TypedDict):",
        "    created_at: str",
        "    id: int",
        "    id_str: str",
        "    text: str",
        "    truncated: bool",
        "    entities: EntitiesType",
        "    source: str",
        "    user: UserType",
        "",
        "RootType = List[RootItemType]",
    ])
    # fmt: on

    assert convert(source, show_imports=True) == expected

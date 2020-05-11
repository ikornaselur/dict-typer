# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_snapshots[json.org.example1] 1'] = '''from typing import List

from typing_extensions import TypedDict


class GlossDef(TypedDict):
    para: str
    GlossSeeAlso: List[str]


class GlossEntry(TypedDict):
    ID: str
    SortAs: str
    GlossTerm: str
    Acronym: str
    Abbrev: str
    GlossDef: GlossDef
    GlossSee: str


class GlossList(TypedDict):
    GlossEntry: GlossEntry


class GlossDiv(TypedDict):
    title: str
    GlossList: GlossList


class Glossary(TypedDict):
    title: str
    GlossDiv: GlossDiv


class Root(TypedDict):
    glossary: Glossary'''

snapshots['test_snapshots[json.org.example2] 1'] = '''from typing import List

from typing_extensions import TypedDict


class MenuitemItem0(TypedDict):
    value: str
    onclick: str


class Popup(TypedDict):
    menuitem: List[MenuitemItem0]


class Menu(TypedDict):
    id: str
    value: str
    popup: Popup


class Root(TypedDict):
    menu: Menu'''

snapshots['test_snapshots[json.org.example3] 1'] = '''from typing_extensions import TypedDict


class Window(TypedDict):
    title: str
    name: str
    width: int
    height: int


class Image(TypedDict):
    src: str
    name: str
    hOffset: int
    vOffset: int
    alignment: str


class Text(TypedDict):
    data: str
    size: int
    style: str
    name: str
    hOffset: int
    vOffset: int
    alignment: str
    onMouseUp: str


class Widget(TypedDict):
    debug: str
    window: Window
    image: Image
    text: Text


class Root(TypedDict):
    widget: Widget'''

snapshots['test_snapshots[json.org.example4] 1'] = '''from typing import List, Union

from typing_extensions import TypedDict


InitParam = TypedDict("InitParam", {
    "configGlossary:installationAt": str,
    "configGlossary:adminEmail": str,
    "configGlossary:poweredBy": str,
    "configGlossary:poweredByIcon": str,
    "configGlossary:staticPath": str,
    "templateProcessorClass": str,
    "templateLoaderClass": str,
    "templatePath": str,
    "templateOverridePath": str,
    "defaultListTemplate": str,
    "defaultFileTemplate": str,
    "useJSP": bool,
    "jspListTemplate": str,
    "jspFileTemplate": str,
    "cachePackageTagsTrack": int,
    "cachePackageTagsStore": int,
    "cachePackageTagsRefresh": int,
    "cacheTemplatesTrack": int,
    "cacheTemplatesStore": int,
    "cacheTemplatesRefresh": int,
    "cachePagesTrack": int,
    "cachePagesStore": int,
    "cachePagesRefresh": int,
    "cachePagesDirtyRead": int,
    "searchEngineListTemplate": str,
    "searchEngineFileTemplate": str,
    "searchEngineRobotsDb": str,
    "useDataStore": bool,
    "dataStoreClass": str,
    "redirectionClass": str,
    "dataStoreName": str,
    "dataStoreDriver": str,
    "dataStoreUrl": str,
    "dataStoreUser": str,
    "dataStorePassword": str,
    "dataStoreTestQuery": str,
    "dataStoreLogFile": str,
    "dataStoreInitConns": int,
    "dataStoreMaxConns": int,
    "dataStoreConnUsageLimit": int,
    "dataStoreLogLevel": str,
    "maxUrlLength": int,
})


class InitParam1(TypedDict):
    mailHost: str
    mailHostOverride: str


class InitParam2(TypedDict):
    templatePath: str
    log: int
    logLocation: str
    logMaxSize: str
    dataLog: int
    dataLogLocation: str
    dataLogMaxSize: str
    removePageCache: str
    removeTemplateCache: str
    fileTransferFolder: str
    lookInContext: int
    adminGroupID: int
    betaServer: bool


ServletItem0 = TypedDict("ServletItem0", {
    "servlet-name": str,
    "servlet-class": str,
    "init-param": Union[InitParam, InitParam1, InitParam2],
})


ServletItem2 = TypedDict("ServletItem2", {
    "servlet-name": str,
    "servlet-class": str,
})


class ServletMapping(TypedDict):
    cofaxCDS: str
    cofaxEmail: str
    cofaxAdmin: str
    fileServlet: str
    cofaxTools: str


Taglib = TypedDict("Taglib", {
    "taglib-uri": str,
    "taglib-location": str,
})


WebApp = TypedDict("WebApp", {
    "servlet": List[Union[ServletItem0, ServletItem2]],
    "servlet-mapping": ServletMapping,
    "taglib": Taglib,
})


Root = TypedDict("Root", {
    "web-app": WebApp,
})'''

snapshots['test_snapshots[json.org.example5] 1'] = '''from typing import List, Union

from typing_extensions import TypedDict


class ItemsItem0(TypedDict):
    id: str


class ItemsItem1(TypedDict):
    id: str
    label: str


class Menu(TypedDict):
    header: str
    items: List[Union[ItemsItem0, ItemsItem1, None]]


class Root(TypedDict):
    menu: Menu'''

snapshots['test_snapshots[sitepoint.com.example1] 1'] = '''from typing import List, Union

from typing_extensions import TypedDict


class Code(TypedDict):
    rgba: List[int]
    hex: str


class ColorsItem0(TypedDict):
    color: str
    category: str
    type: str
    code: Code


class ColorsItem1(TypedDict):
    color: str
    category: str
    code: Code


class Root(TypedDict):
    colors: List[Union[ColorsItem0, ColorsItem1]]'''

snapshots['test_snapshots[sitepoint.com.example2] 1'] = '''from typing import List, Union

from typing_extensions import TypedDict


class MarkersItem0(TypedDict):
    name: str
    position: List[float]


class MarkersItem1(TypedDict):
    name: str
    location: List[float]


class Root(TypedDict):
    markers: List[Union[MarkersItem0, MarkersItem1]]'''

snapshots['test_snapshots[sitepoint.com.example3] 1'] = '''from typing import List, Union

from typing_extensions import TypedDict


class PageInfo(TypedDict):
    totalResults: int
    resultsPerPage: int


class Id(TypedDict):
    kind: str
    channelId: str


class Id1(TypedDict):
    kind: str
    videoId: str


class ItemsItem0(TypedDict):
    kind: str
    etag: str
    id: Union[Id, Id1]


class Root(TypedDict):
    kind: str
    etag: str
    nextPageToken: str
    regionCode: str
    pageInfo: PageInfo
    items: List[ItemsItem0]'''

snapshots['test_snapshots[sitepoint.com.example4] 1'] = '''from typing import List, Union

from typing_extensions import TypedDict


class HashtagsItem0(TypedDict):
    text: str
    indices: List[int]


class UrlsItem0(TypedDict):
    url: str
    expanded_url: str
    display_url: str
    indices: List[int]


class Entities(TypedDict):
    hashtags: List[HashtagsItem0]
    symbols: List
    user_mentions: List
    urls: List[UrlsItem0]


class Url(TypedDict):
    urls: Union[List, List[UrlsItem0]]


class Entities1(TypedDict):
    url: Url
    description: Url


class User(TypedDict):
    id: int
    id_str: str
    name: str
    screen_name: str
    location: str
    description: str
    url: str
    entities: Entities1
    protected: bool
    followers_count: int
    friends_count: int
    listed_count: int
    created_at: str
    favourites_count: int
    utc_offset: int
    time_zone: str


class RootItem0(TypedDict):
    created_at: str
    id: int
    id_str: str
    text: str
    truncated: bool
    entities: Entities
    source: str
    user: User


Root = List[RootItem0]'''

snapshots['test_snapshots[custom.example1] 1'] = '''from typing import List, Union

from typing_extensions import TypedDict


class DataItem0(TypedDict):
    timestamp: str
    text: str
    id: str


class Comments(TypedDict):
    data: Union[List[DataItem01], List[DataItem0]]


class Owner(TypedDict):
    id: str


class Cursors(TypedDict):
    after: str


class Paging(TypedDict):
    cursors: Cursors
    next: str


class Comments1(TypedDict):
    data: List[DataItem0]
    paging: Paging


class RootItem0(TypedDict):
    caption: str
    comments: Union[Comments, Comments1]
    comments_count: int
    id: str
    ig_id: str
    is_comment_enabled: bool
    like_count: int
    media_type: str
    media_url: str
    owner: Owner
    permalink: str
    shortcode: str
    timestamp: str
    username: str


class RootItem1(TypedDict):
    caption: str
    children: Comments
    comments: Union[Comments, Comments1]
    comments_count: int
    id: str
    ig_id: str
    is_comment_enabled: bool
    like_count: int
    media_type: str
    media_url: str
    owner: Owner
    permalink: str
    shortcode: str
    timestamp: str
    username: str


Root = List[Union[RootItem0, RootItem1]]'''

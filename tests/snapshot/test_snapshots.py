import json
from typing import Any, Dict, List, Union

import pytest

from dict_typer import get_type_definitions


def get_f(num: int) -> Union[Dict, List]:
    with open(f"tests/snapshot/fixtures/json.org.example{num}.json", "r") as f:
        return json.load(f)


def sitepoint_com_fixture(num: int) -> Union[Dict, List]:
    with open(f"tests/snapshot/fixtures/sitepoint.com.example{num}.json", "r") as f:
        return json.load(f)


@pytest.mark.parametrize(
    "fixture",
    [
        "json.org.example1",
        "json.org.example2",
        "json.org.example3",
        "json.org.example4",
        "json.org.example5",
        "sitepoint.com.example1",
        "sitepoint.com.example2",
        "sitepoint.com.example3",
        "sitepoint.com.example4",
        "custom.example1",
    ],
)
def test_snapshots(snapshot: Any, fixture: str) -> None:
    with open(f"tests/snapshot/fixtures/{fixture}.json", "r") as f:
        source = json.load(f)

    output = get_type_definitions(source)

    snapshot.assert_match(output)

from typing import List

import pytest

from dict_typer.types import get_type


@pytest.mark.parametrize(
    "data,expected_type",
    [
        ([True, False], "bool"),
        ([bytearray([102, 111, 111]), bytearray("foo", "utf-8")], "bytearray"),
        ([b"foo", b"bar"], "bytes"),
        ([1j, -2j], "complex"),
        ([enumerate(["a", "b", "c"])], "enumerate"),
        ([1.0, 0.2], "float"),
        ([-1, 0, 3], "int"),
        ([memoryview(b"foo"), memoryview(b"bar")], "memoryview"),
        ([range(1, 10), range(30)], "range"),
        (["foo", "bar"], "str"),
        ([str, float, int], "type"),
        ([filter(lambda x: x < 10, range(20))], "filter"),
        ([map(lambda x: x * 2, range(20))], "map"),
        ([zip([1, 2], [3, 4])], "zip"),
        ([[1, 2], ["a", "b"]], "List"),
        ([(1, 2), ("a", "b")], "Tuple"),
        ([{1, 2}, {"a", "b"}], "Set"),
        ([frozenset([1, 2]), frozenset(["a", "b"])], "FrozenSet"),
        ([{"foo": "bar"}, {"baz": 123}], "Dict"),
    ],
)
def test_get_type(data: List, expected_type: str) -> None:
    for item in data:
        assert get_type(item) == expected_type

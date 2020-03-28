from keyword import kwlist

from dict_typer.utils import is_valid_key


def test_is_valid_key_with_valid_names() -> None:
    keys = ["foo", "foo_bar", "fooBar", "number3", "FOO"]

    assert all(is_valid_key(key) for key in keys)


def test_is_valid_key_rejects_keywords() -> None:
    assert not any(is_valid_key(key) for key in kwlist)


def test_is_valid_key_rejects_invalid_identifiers() -> None:
    keys = ["foo-bar", "123" "?", "a space"]

    assert not any(is_valid_key(key) for key in keys)

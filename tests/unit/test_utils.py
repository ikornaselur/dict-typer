from keyword import kwlist

from dict_typer.utils import is_valid_key, key_to_class_name


def test_is_valid_key_with_valid_names() -> None:
    keys = ["foo", "foo_bar", "fooBar", "number3", "FOO"]

    assert all(is_valid_key(key) for key in keys)


def test_is_valid_key_rejects_keywords() -> None:
    assert not any(is_valid_key(key) for key in kwlist)


def test_is_valid_key_rejects_invalid_identifiers() -> None:
    keys = ["foo-bar", "123" "?", "a space"]

    assert not any(is_valid_key(key) for key in keys)


def test_key_to_class_name_with_valid_names() -> None:
    assert key_to_class_name("foo") == "Foo"
    assert key_to_class_name("foo_bar") == "FooBar"
    assert key_to_class_name("FOO") == "Foo"


def test_key_to_class_name_with_reserved_keywords_names() -> None:
    assert key_to_class_name("from") == "From"
    assert key_to_class_name("async") == "Async"


def test_key_to_class_name_with_non_valid_identifiers() -> None:
    assert key_to_class_name("foo-bar") == "FooBar"
    assert key_to_class_name("baz qux") == "BazQux"


def test_key_to_class_name_with_repeated_splits() -> None:
    assert key_to_class_name("foo-----bar") == "FooBar"
    assert key_to_class_name("baz_____qux") == "BazQux"
    assert key_to_class_name("_____bar") == "Bar"


def test_key_to_class_name_camel_case_already() -> None:
    assert key_to_class_name("fooBar") == "FooBar"
    assert key_to_class_name("BazQux") == "BazQux"

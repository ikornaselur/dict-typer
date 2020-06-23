from dict_typer.models import DictEntry, MemberEntry, key_to_dependency_cmp
from dict_typer.utils import get_imports


def test_member_entry_base_output() -> None:
    entry = MemberEntry("str")

    assert str(entry) == "str"


def test_member_entry_sub_types() -> None:
    entry = MemberEntry("List", sub_members={MemberEntry("str")})

    assert str(entry) == "List[str]"


def test_member_entry_sub_types_union() -> None:
    entry = MemberEntry("List", sub_members={MemberEntry("str"), MemberEntry("int")})

    assert str(entry) == "List[Union[int, str]]"


def test_member_entry_sub_types_optional_if_just_one_type() -> None:
    entry = MemberEntry("List", sub_members={MemberEntry("str"), MemberEntry("None")})

    assert str(entry) == "List[Optional[str]]"


def test_member_entry_sub_types_union_instead_of_optional_if_multiple_types() -> None:
    entry = MemberEntry(
        "List",
        sub_members={MemberEntry("str"), MemberEntry("int"), MemberEntry("None")},
    )

    assert str(entry) == "List[Union[None, int, str]]"


def test_member_entry_is_hashable_based_on_str_out() -> None:
    assert hash(MemberEntry("int")) == hash(MemberEntry("int"))

    hashed_list_int_1 = hash(MemberEntry("List", sub_members={MemberEntry("int")}))
    hashed_list_int_2 = hash(MemberEntry("List", sub_members={MemberEntry("int")}))
    hashed_list_str = hash(MemberEntry("List", sub_members={MemberEntry("str")}))

    assert hashed_list_int_1 == hashed_list_int_2
    assert hashed_list_int_1 != hashed_list_str

    assert {MemberEntry("int"), MemberEntry("int"), MemberEntry("int")} == {
        MemberEntry("int")
    }


def test_member_entry_imports() -> None:
    just_list = MemberEntry("List")
    just_list_one_item = MemberEntry("List", sub_members={MemberEntry("str")})
    list_with_union = MemberEntry(
        "List", sub_members={MemberEntry("str"), MemberEntry("int")}
    )
    list_with_optional = MemberEntry(
        "List", sub_members={MemberEntry("str"), MemberEntry("None")}
    )

    assert just_list.imports == {"List"}
    assert just_list_one_item.imports == {"List"}
    assert list_with_union.imports == {"List", "Union"}
    assert list_with_optional.imports == {"List", "Optional"}


def test_member_entry_get_imports_from_sub_members() -> None:
    sub_entry = DictEntry(
        "NestedType",
        members={
            "foo": {
                MemberEntry(
                    "List", sub_members={MemberEntry("int"), MemberEntry("str")}
                )
            }
        },
    )
    entry = MemberEntry(
        "List",
        sub_members={sub_entry, MemberEntry("Set", sub_members={MemberEntry("int")})},
    )

    assert get_imports(entry) == {"List", "Union", "Set"}


def test_dict_entry_base_output() -> None:
    entry = DictEntry(
        "RootType", members={"foo": {MemberEntry("str")}, "bar": {MemberEntry("int")}}
    )

    # fmt: off
    assert str(entry) == "\n".join([
        "class RootType(TypedDict):",
        "    foo: str",
        "    bar: int",
    ])
    # fmt: on


def test_dict_entry_nested_dicts() -> None:
    sub_entry = DictEntry(
        "NestedType",
        members={
            "foo": {
                MemberEntry(
                    "List", sub_members={MemberEntry("int"), MemberEntry("str")}
                )
            }
        },
    )
    entry = DictEntry("RootType", members={"sub": {sub_entry}})

    # fmt: off
    assert str(entry) == "\n".join([
        "class RootType(TypedDict):",
        "    sub: NestedType",
    ])
    # fmt: on


def test_dict_entry_alternative_output() -> None:
    entry = DictEntry(
        "RootType",
        members={"foo": {MemberEntry("str")}, "bar": {MemberEntry("int")}},
        force_alternative=True,
    )

    # fmt: off
    assert str(entry) == "\n".join([
        'RootType = TypedDict("RootType", {',
        '    "foo": str,',
        '    "bar": int,',
        '})',
    ])
    # fmt: on


def test_member_entry_with_dict_entry() -> None:
    dict_entry = DictEntry("SubType", members={"foo": {MemberEntry("str")}})
    entry = MemberEntry("List", sub_members={dict_entry})

    assert str(entry) == "List[SubType]"


def test_dict_entry_with_member_entry() -> None:
    dict_entry = DictEntry("SubType", members={"foo": {MemberEntry("str")}})
    member_entry = MemberEntry("List", sub_members={dict_entry})
    entry = MemberEntry("Set", sub_members={member_entry})

    assert str(entry) == "Set[List[SubType]]"


def test_dict_entry_get_imports() -> None:
    base_entry = DictEntry("RootType", members={"foo": {MemberEntry("str")}})
    base_entry_with_list = DictEntry(
        "RootType",
        members={
            "bar": {
                MemberEntry(
                    "List", sub_members={MemberEntry("int"), MemberEntry("str")}
                )
            }
        },
    )

    assert get_imports(base_entry) == set()
    assert get_imports(base_entry_with_list) == {"List", "Union"}


def test_dict_entry_get_imports_from_sub_members() -> None:
    sub_entry = DictEntry(
        "NestedType",
        members={
            "foo": {
                MemberEntry(
                    "List", sub_members={MemberEntry("int"), MemberEntry("str")}
                )
            }
        },
    )
    entry = DictEntry("RootType", members={"sub": {sub_entry}})

    assert get_imports(entry) == {"List", "Union"}


def test_sorting_member_entries_based_on_dependency() -> None:
    foo = MemberEntry(name="Foo")
    bar = MemberEntry(name="Bar", sub_members={foo})
    baz = MemberEntry(name="Baz", sub_members={bar})

    assert sorted([foo, bar, baz], key=key_to_dependency_cmp) == [foo, bar, baz]
    assert sorted([bar, foo, baz], key=key_to_dependency_cmp) == [foo, bar, baz]
    assert sorted([baz, bar, foo], key=key_to_dependency_cmp) == [foo, bar, baz]


def test_sorting_dict_entry_based_on_dependency() -> None:
    foo = MemberEntry(name="Foo")
    bar = MemberEntry(name="Bar", sub_members={foo})
    baz = MemberEntry(name="int")

    entry = DictEntry("RootType", members={"foo": {foo}, "bar": {bar}, "baz": {baz}})

    assert sorted([foo, baz, entry, bar], key=key_to_dependency_cmp) == [
        foo,
        baz,
        bar,
        entry,
    ]


def test_sorting_dict_entry_with_sub_entry() -> None:
    sub_entry = DictEntry(
        "NestedType",
        members={
            "foo": {
                MemberEntry(
                    "List", sub_members={MemberEntry("int"), MemberEntry("str")}
                )
            }
        },
    )
    entry = DictEntry("RootType", members={"sub": {sub_entry}})

    assert sub_entry.name in entry.depends_on
    assert entry.name not in sub_entry.depends_on

    assert sorted([entry, sub_entry], key=key_to_dependency_cmp) == [sub_entry, entry]
    assert sorted([sub_entry, entry], key=key_to_dependency_cmp) == [sub_entry, entry]


def test_dict_entry_invalid_name_adds_underscore() -> None:
    assert DictEntry("List").name == "List_"
    assert DictEntry("None").name == "None_"

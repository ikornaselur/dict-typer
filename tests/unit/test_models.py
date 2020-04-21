from dict_typer.models import DictEntry, MemberEntry


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


def test_dict_entry_base_output() -> None:
    entry = DictEntry(
        "RootType", members={"foo": MemberEntry("str"), "bar": MemberEntry("int")}
    )

    # fmt: off
    assert str(entry) == "\n".join([
        "class RootType(TypedDict):",
        "    foo: str",
        "    bar: int",
    ])
    # fmt: on


def test_dict_entry_alternative_output() -> None:
    entry = DictEntry(
        "RootType",
        members={"foo": MemberEntry("str"), "bar": MemberEntry("int")},
        force_alternative=True,
    )

    # fmt: off
    assert str(entry) == "\n".join([
        'RootType = TypedDict("RootType", {',
        '    "foo": str',
        '    "bar": int',
        '})',
    ])
    # fmt: on


def test_member_entry_with_dict_entry() -> None:
    dict_entry = DictEntry("SubType", members={"foo": MemberEntry("str")})
    entry = MemberEntry("List", sub_members={dict_entry})

    assert str(entry) == "List[SubType]"


def test_dict_entry_with_member_entry() -> None:
    dict_entry = DictEntry("SubType", members={"foo": MemberEntry("str")})
    member_entry = MemberEntry("List", sub_members={dict_entry})
    entry = MemberEntry("Set", sub_members={member_entry})

    assert str(entry) == "Set[List[SubType]]"

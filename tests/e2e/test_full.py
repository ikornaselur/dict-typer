import subprocess
import tempfile

from dict_typer import convert

# fmt: off
TEST_SOURCE = {
    "foo": "bar",
    "items": [1, "2", 3.0],
    "nested": {
        "id": 1,
        "value": "val",
    },
    "same_type_other_nested": {
        "id": 2,
        "value": "hello",
    },
    "subsets": {
        "first": {1, 2},
        "second": {3, 4},
        "third": {5, 6},
    },
    "nestedInvalid": {
        "foo-bar": "string",
        "from": "far away",
    }
}
# fmt: on


def _line_numbered(string: str) -> str:
    lines = string.split("\n")
    return "\n".join([f"{idx+1:2}: {line}" for idx, line in enumerate(lines)])


def test_script_runs_with_nonzero() -> None:
    """ A python e2e test

    1. Takes a source and converts it to a definition
    2. Adds a simple script to use the Type
    3. Saves the definition output into a Python file
    4. Runs the file to verify it runs
    """

    # 1.
    source_type_name = "Test"
    type_postfix = "Type"

    output = convert(
        TEST_SOURCE,
        root_type_name=source_type_name,
        type_postfix=type_postfix,
        show_imports=True,
    )

    # 2.
    input_string = f"test_source: {source_type_name}{type_postfix} = {TEST_SOURCE}"
    # fmt: off
    output += "\n".join([
        "",
        "",
        f"{input_string}",
        "print(test_source)",
    ])
    # fmt: on

    # 3.
    with tempfile.NamedTemporaryFile(suffix=".py") as f:
        f.write(output.encode("utf-8"))
        f.flush()

        # 4.
        with subprocess.Popen(["python", f.name], stdout=subprocess.PIPE) as proc:
            stdout, stderr = proc.communicate()
            assert not proc.returncode, "\n".join(
                [
                    "Non zero return code from script.",
                    "stderr:",
                    stderr and stderr.decode("utf-8") or "",
                    "Full script:",
                    "-" * 60,
                    _line_numbered(output),
                    "-" * 60,
                ]
            )

            assert stdout.decode("utf-8") == f"{TEST_SOURCE}\n"


def test_mypy_has_no_issues() -> None:
    """ A mypy e2e test

    1. Takes a source and converts it to a definition
    2. Adds a simple script to use the Type
    3. Saves the definition output into a Python file
    4. Runs mypy on the script to verify there are no typing issues
    """

    # 1.
    source_type_name = "Test"
    type_postfix = "Type"

    output = convert(
        TEST_SOURCE,
        root_type_name=source_type_name,
        type_postfix=type_postfix,
        show_imports=True,
    )

    # 2.
    input_string = f"test_source: {source_type_name}{type_postfix} = {TEST_SOURCE}"
    # fmt: off
    output += "\n".join([
        "",
        "",
        f"{input_string}",
        "print(test_source)",
    ])
    # fmt: on

    # 3.
    with tempfile.NamedTemporaryFile(suffix=".py") as f:
        f.write(output.encode("utf-8"))
        f.flush()

        # 4.

        # 4.
        with subprocess.Popen(["mypy", f.name], stdout=subprocess.PIPE) as proc:
            stdout, stderr = proc.communicate()
            assert not proc.returncode, "\n".join(
                ["Non zero return code from mypy.", "stderr:", stderr.decode("utf-8")]
            )

            assert (
                stdout.decode("utf-8") == "Success: no issues found in 1 source file\n"
            )

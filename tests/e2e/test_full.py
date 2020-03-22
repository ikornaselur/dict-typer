import subprocess
import tempfile

from dict_typer import convert

TEST_SOURCE = {"foo": "bar", "items": [1, "2", 3.0]}


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
        source_type_name=source_type_name,
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
        result = subprocess.run(["python", f.name], capture_output=True)
        returncode = result.returncode
        assert (
            returncode == 0
        ), f"Non zero return code from script. stderr: \n\n{result.stderr.decode('utf-8')}"

        stdout = result.stdout.decode("utf-8")
        assert stdout == f"{TEST_SOURCE}\n"


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
        source_type_name=source_type_name,
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
        result = subprocess.run(["mypy", f.name], capture_output=True)
        returncode = result.returncode
        assert (
            returncode == 0
        ), f"Non zero return code from script. stderr: \n\n{result.stdout.decode('utf-8')}"

        stdout = result.stdout.decode("utf-8")
        assert stdout == "Success: no issues found in 1 source file\n"

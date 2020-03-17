import sys

from dict_typer.convert import ConvertException, convert


def dict_typer() -> None:
    if sys.stdin.isatty():
        print("Pipe dictionary instance dict-typer")
        sys.exit(1)

    stream = sys.stdin.read()

    try:
        output = convert(stream)
    except ConvertException as e:
        print(str(e))
        sys.exit(2)

    print(output)

import io
import json
import sys
from typing import Dict, Tuple

import click

from dict_typer.convert import convert

__version__ = "0.1.5"


@click.command()
@click.option(
    "--imports/--no-imports",
    default=True,
    help="Show imports at the top, default: True",
)
@click.argument("file", type=click.File("r"), nargs=-1)
@click.version_option(__version__)
def cli(file: Tuple[io.TextIOWrapper], imports: bool = True) -> None:
    if len(file) > 1:
        raise click.BadArgumentUsage("Multiple files supplied, run with one at a time")
    if len(file) == 0:
        if sys.stdin.isatty():
            raise click.UsageError(
                "Either provide the path to the file or pipe a file to dict-typer"
            )
        else:
            stream = sys.stdin.read().strip()
    else:
        stream = file[0].read().strip()

    try:
        parsed: Dict = json.loads(stream)
    except json.decoder.JSONDecodeError as e:
        raise click.UsageError(f"JSON serialisation error \n\n{e}")

    output = convert(parsed, show_imports=imports)

    click.echo(output)

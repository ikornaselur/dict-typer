import io
import json
import sys
from typing import Dict, Tuple

import click
from rich.console import Console
from rich.syntax import Syntax

from dict_typer.type_definitions import get_type_definitions

__version__ = "0.1.15"


@click.command()
@click.option(
    "--imports/--no-imports",
    default=True,
    help="Show imports at the top, default: True",
)
@click.option("--rich", "-r", is_flag=True, help="Show rich output.")
@click.option(
    "--line-numbers", "-l", is_flag=True, help="Show line numbers if rich.",
)
@click.argument("file", type=click.File("r"), nargs=-1)
@click.version_option(__version__)
def cli(
    file: Tuple[io.TextIOWrapper],
    imports: bool = True,
    rich: bool = False,
    line_numbers: bool = False,
) -> None:
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

    output = get_type_definitions(parsed, show_imports=imports)
    if rich:
        syntax = Syntax(output, "python", theme="monokai", line_numbers=line_numbers)
        console = Console()
        console.print(syntax)
    else:
        click.echo(output)

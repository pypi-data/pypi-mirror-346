from typing import Annotated, Any, Callable, List, Optional

import click
import typer
from merge_args import merge_args  # type: ignore
from typer import Argument, Option

from airfold_cli._pydantic import BaseModel, Extra
from airfold_cli.completion import (
    ai_source_name_completion,
    importable_database_name_completion,
    importable_table_name_completion,
    job_ids_completion,
    source_name_completion,
)
from airfold_cli.models import NamedParam, OutputDataFormat

GLOBAL_OPTIONS_PANEL_NAME = "Global options"

InteractivePromptOption: bool = Option(
    "--prompt", help="Force toggle prompts for this CLI run.", rich_help_panel=GLOBAL_OPTIONS_PANEL_NAME
)
"""If `True`, use interactive prompts in CLI commands. If `False`, no interactive
prompts will be used.
"""

VerbosityOption: Optional[int] = Option(
    "--verbose",
    "-v",
    help="Set verbosity level, can be repeated.",
    count=True,
    rich_help_panel=GLOBAL_OPTIONS_PANEL_NAME,
)

PathArgument: Optional[List[str]] = Argument(
    file_okay=True, dir_okay=True, help="Path to a local object file(s), ('-' will read objects from stdin)."
)

PathArgumentNoStream: Optional[List[str]] = Argument(
    file_okay=True, dir_okay=True, help="Path to a local object file(s)."
)

PathOrURL: Optional[str] = Argument(file_okay=True, dir_okay=True, help="Path to a local file or URL.")
PathsOrURLs: Optional[List[str]] = Argument(file_okay=True, dir_okay=True, help="Path to a local file(s) or URL(s).")

SourceNameArgument: str = Argument(help="Source name", autocompletion=source_name_completion)
AISourceNameArgument: str = Argument(help="Source name", autocompletion=ai_source_name_completion)

ApplyOption: bool = Option(
    "--apply",
    help="Apply the pushed pipeline, default is to plan only.",
)

ForceOption: bool = Option(
    "--force",
    help="Force delete/overwrite even if data will be lost.",
)

OverwriteFileOption: bool = Option(
    "--overwrite",
    help="Overwrite existing local file(s) without confirmation.",
)

DryRunOption: bool = Option(
    "--dry-run",
    help="Show execution plan without executing it.",
)

WaitOption: bool = Option(
    "--wait",
    help="Wait for the operation to complete.",
)

TargetDir: Optional[str] = Argument(
    file_okay=False,
    dir_okay=True,
    help="Target directory to create files in, ('-' will dump to stdout). Preserves airfold layout.",
)

OutputPathArgument: str = Argument(file_okay=True, dir_okay=True, help="Output path, ('-' will dump to stdout).")

OutputDataFormatOption: OutputDataFormat = Option(
    "--format",
    "-f",
    help="Output data format.",
)

FixOption: bool = Option(
    "--fix",
    help="Fix issues automatically",
)

ListChecksOption: bool = Option(
    "--list-checks",
    help="List available checks",
)


class NamedParamParser(click.ParamType):
    def __init__(self, name: str = "NAME=VALUE") -> None:
        self.name = name

    def convert(self, value, param, ctx):
        try:
            key, value = value.split("=", 1)
            return NamedParam(name=key, value=value)
        except Exception:
            raise typer.BadParameter(f"{value} is not a valid name=value pair") from None


PipeParamOption: Optional[list[NamedParam]] = Option(
    "--param",
    "-p",
    help="Set pipe parameters.",
    click_type=NamedParamParser(),
)


PushRenameOption: Optional[list[NamedParam]] = Option(
    "--rename",
    "-r",
    help="Use `rename` strategy. Specify a single renamed object name and its new name.",
    click_type=NamedParamParser(name="NAME=NEW_NAME"),
)

NameOption: Optional[list[str]] = Option(
    "--name",
    "-n",
    help="Object name(s).",
)

ImportAsOption: Optional[str] = Option(
    "--as",
    help="Import source as. If not specified, table name will be used.",
)

ImportTableArgument: str = Argument(
    help="Table to import.",
    autocompletion=importable_table_name_completion,
)

ImportDbArgument: str = Argument(
    help="Database to import table from.",
    autocompletion=importable_database_name_completion,
)

OutSourcePath: Optional[str] = Option("--out", help="New source output path, ex.: sources/src1.yaml.")

JobIdArgument: str = Argument(help="Job ID.", autocompletion=job_ids_completion)

MaxWaitOption: Optional[int] = Option(
    "--max-wait",
    help="Maximum wait time in seconds.",
)

PipeNodeNameOption: Optional[str] = Option(
    "--node",
    "-n",
    help="Node name.",
)


class GlobalOptions(BaseModel):
    verbose: Optional[int] = 0
    prompt: Optional[bool] = None

    def update_from_dict(self, d: dict[str, Any]):
        for k, v in d.items():
            if hasattr(self, k) and v is not None:
                setattr(self, k, v)

    class Config:
        arbitrary_types_allowed = True
        extra = Extra.allow


def with_global_options(
    func: Callable,
) -> Callable:
    """Decorator to add global options to a command."""

    options = GlobalOptions()

    @merge_args(func)
    def wrapper(
        *args,
        # should be None by default to prevent overwriting config if an option was specified before a sub-command.
        prompt: Annotated[Optional[bool], InteractivePromptOption] = options.prompt,
        verbose: Annotated[Optional[int], VerbosityOption] = options.verbose,
        **kwargs,
    ):
        return func(*args, **kwargs)

    return wrapper

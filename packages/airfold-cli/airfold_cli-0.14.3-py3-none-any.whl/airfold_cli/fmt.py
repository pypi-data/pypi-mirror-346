from enum import Enum
from pathlib import Path
from typing import Annotated, List, Optional, Union

import yaml
from airfold_common.project import (
    TRAILING_SPACE_RE,
    LocalFile,
    ProjectFile,
    create_file,
    dump_yaml,
    find_project_files,
)
from airfold_common.utils import is_path_stream
from deepdiff import DeepDiff  # type: ignore
from rich.console import Console, ConsoleOptions, RenderResult
from rich.markup import escape
from rich.rule import Rule
from rich.syntax import Syntax
from typer import Context

from airfold_cli.api import AirfoldApi
from airfold_cli.error import AirfoldError
from airfold_cli.options import (
    DryRunOption,
    OverwriteFileOption,
    PathArgumentNoStream,
    with_global_options,
)
from airfold_cli.prompts import prompt_overwrite_local_file
from airfold_cli.root import app, catch_airfold_error
from airfold_cli.tui.syntax import get_syntax_theme
from airfold_cli.utils import normalize_name, normalize_path_args


class FormatStatus(str, Enum):
    FIXED = "Fixed"
    REFORMATTED = "Reformatted"
    UNCHANGED = "Unchanged"


class FileHeader:
    def __init__(self, status: FormatStatus, file_path: Union[str, Path]):
        self.file_path = file_path
        self.status = status
        if status == FormatStatus.FIXED:
            self.path_prefix = f"[bold green]{status.value} [/]"
        elif status == FormatStatus.REFORMATTED:
            self.path_prefix = f"[bold blue]{status.value} [/]"
        else:
            self.path_prefix = ""

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        yield Rule(
            f"{self.path_prefix}[b]{escape(str(self.file_path))}[/]",
            style="border",
            characters="▁",
        )


class UnchangedFileBody:
    """Represents a file that was not changed."""

    def __init__(self, file_path: Union[str, Path]):
        self.file = file_path

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        yield Rule(characters="╲", style="hatched")
        yield Rule(" [blue]File was not changed ", characters="╲", style="hatched")
        yield Rule(characters="╲", style="hatched")
        yield Rule(style="border", characters="▔")


def load_file_strip_space(path: Path) -> list[LocalFile]:
    res: list[LocalFile] = []
    data = open(path).read()
    data = TRAILING_SPACE_RE.sub("", data)
    docs = list(yaml.safe_load_all(data))
    if len(docs) > 1:
        for doc in docs:
            res.append(create_file(doc, str(path)))
    elif len(docs) == 1:
        res.append(LocalFile(name=path.stem, data=docs[0], path=str(path)))
    return res


@app.command("fmt")
@catch_airfold_error()
@with_global_options
def fmt(
    ctx: Context,
    path: Annotated[Optional[List[str]], PathArgumentNoStream] = None,
    dry_run: Annotated[bool, DryRunOption] = False,
    overwrite: Annotated[bool, OverwriteFileOption] = False,
) -> None:
    """Format local object files.
    \f

    Args:
        ctx: Typer context
        path: path to local object file(s)
        dry_run: print formatted files to stdout without saving them
        overwrite: overwrite existing files
    """
    app.apply_options(ctx)

    if not app.is_interactive() and not dry_run and not overwrite:
        raise AirfoldError("Use --overwrite in non-interactive mode")

    if dry_run and overwrite:
        app.ui.print_warning("--dry-run and --overwrite are mutually exclusive, ignoring --overwrite")

    args = normalize_path_args(path)
    paths: list[Path] = find_project_files(args)

    name_to_path: dict[str, LocalFile] = {}
    files: list[ProjectFile] = []
    for local_file in paths:
        # ignore stdin
        if is_path_stream(local_file):
            app.ui.print_warning(f"Reading from stdin is not allowed. Skipped.")
            continue
        project_files = load_file_strip_space(local_file)
        for pf in project_files:
            npf = ProjectFile(name=pf.name, data=normalize_name(pf.data.copy(), pf.name))
            lf = LocalFile(**pf.dict(exclude={"path"}), path=str(local_file))
            files.append(pf)
            name_to_path[npf.data["name"]] = lf

    api = AirfoldApi.from_config()
    lint_result = api.lint(files, False, False)
    if lint_result.errors:
        errors = "\n".join([f"  - {e}" for e in lint_result.errors])
        app.ui.print_error(f"Found {len(lint_result.errors)} errors in the files: {errors}")
        return

    formatted_files_map: dict[str, list[ProjectFile]] = {}
    for normalized_file in lint_result.files:
        original_file = name_to_path[normalized_file.data["name"]]
        if original_file.path not in formatted_files_map:
            formatted_files_map[original_file.path] = []
        formatted_files_map[original_file.path].append(normalized_file)

    for local_file_path, formatted_files in formatted_files_map.items():
        format_status: FormatStatus = FormatStatus.UNCHANGED
        for fpf in formatted_files:
            original_file = name_to_path[fpf.data["name"]]
            ddiff = DeepDiff(original_file.data, fpf.data, exclude_paths=["name"])
            if ddiff:
                format_status = FormatStatus.FIXED

        yaml_data: str = dump_yaml([ff.data.copy() for ff in formatted_files], remove_names=len(formatted_files) == 1)
        if app.is_terminal():
            if format_status == FormatStatus.UNCHANGED:
                with open(local_file_path, "r") as f:
                    raw_data = f.read()
                    if raw_data != yaml_data:
                        format_status = FormatStatus.REFORMATTED

            app.console.print(FileHeader(format_status, local_file_path))
            if format_status == FormatStatus.UNCHANGED:
                app.console.print(UnchangedFileBody(local_file_path))
                continue
            else:
                app.console.print(Syntax(yaml_data, "yaml", theme=get_syntax_theme()))
        else:
            app.console.print("---\n" + dump_yaml([ff.data for ff in formatted_files], remove_names=False))

        if dry_run:
            continue

        store: bool = True
        if not overwrite:
            store = prompt_overwrite_local_file(str(local_file_path), console=app.console)

        if not store:
            continue

        with open(local_file_path, "w") as f:
            f.write(yaml_data)

from collections.abc import Sequence
from pathlib import Path
import click

from lint_utils._cli_commands.check import CheckCommand
from lint_utils.config import PyProject
from lint_utils.std import report_info
from lint_utils.text_styling import pluralize, to_bold, to_green, to_red
from lint_utils.timer import Timer


@click.group()
def cli() -> None:
    pass


@cli.command("check")
@click.argument("args", nargs=-1)
def check(args: Sequence[str]) -> None:
    pyproject = PyProject.from_toml(Path("pyproject.toml"))
    lint_utils_config = (
        pyproject.tool.lint_utils if pyproject and pyproject.tool else None
    )

    files_count = 0
    errors_files_count = 0
    not_processed_files: list[str] = []

    if not args:
        report_info(to_red("Please provide the file or directory name"))
        return

    with Timer() as timer:
        for arg in args:
            root_path = Path(arg)
            paths = root_path.rglob("*.py") if root_path.is_dir() else (root_path,)
            command = CheckCommand(paths=paths, config=lint_utils_config)
            result = command.execute()

            not_processed_files.extend(result.not_processed_files)
            files_count += result.files_count
            errors_files_count += result.errors_files_count

    if errors_files_count > 0:
        files_part = pluralize(errors_files_count, "file")
        msg = to_bold(
            to_red(f"Errors found in {errors_files_count} {files_part} 😱")
        )
        report_info(msg)
    else:
        report_info(to_bold(to_green("No errors found. All is well 🤗")))

    total_info = f"Processed {files_count} {pluralize(files_count, 'file')} at {timer.total_seconds}"
    report_info(to_bold((total_info)))


if __name__ == "__main__":
    cli()

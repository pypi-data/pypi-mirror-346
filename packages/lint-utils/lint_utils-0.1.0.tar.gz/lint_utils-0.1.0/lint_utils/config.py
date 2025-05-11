from pathlib import Path
from typing import Self
import msgspec

from lint_utils.std import report_error


class Base(
    msgspec.Struct,
    omit_defaults=True,
    forbid_unknown_fields=False,
):
    pass


class LintConfig(Base):
    ignore: list[str] = msgspec.field(default_factory=list)
    exclude_classes: list[str] = msgspec.field(default_factory=list)
    exclude_base_classes: list[str] = msgspec.field(default_factory=list)


class LintUtilsConfig(Base):
    lint: LintConfig = msgspec.field(default_factory=LintConfig)
    exclude: list[str] = msgspec.field(default_factory=list)


class Tool(Base):
    lint_utils: LintUtilsConfig | None = None


class PyProject(Base):
    tool: Tool | None = None

    @classmethod
    def from_toml(cls, path: Path) -> Self | None:
        try:
            with path.open("r", encoding="UTF-8") as file:
                return msgspec.toml.decode(file.read(), type=PyProject)
        except OSError as exc:
            if isinstance(exc, FileNotFoundError):
                return None

            msg = f"There was a problem parsing the file pyproject.toml. Error: {repr(exc)}"
            report_error(msg)

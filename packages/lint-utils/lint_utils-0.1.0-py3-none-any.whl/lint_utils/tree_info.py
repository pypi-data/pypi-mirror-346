from contextlib import suppress
from pathlib import Path

import ast
from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class TreeInfo:
    tree: ast.Module
    raw: str


def get_tree_info(file_path: Path) -> TreeInfo | None:
    with suppress(SyntaxError, OSError, UnicodeDecodeError), file_path.open("r", encoding="UTF-8") as file:
        source = file.read()
        return TreeInfo(tree=ast.parse(source), raw=source)

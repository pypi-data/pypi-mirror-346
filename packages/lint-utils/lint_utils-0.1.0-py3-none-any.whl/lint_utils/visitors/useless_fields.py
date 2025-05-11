import ast
from dataclasses import dataclass
import itertools
from pathlib import Path
from typing import Any, Final, Mapping, TypeAlias

from lint_utils.config import LintUtilsConfig
from lint_utils.rules import Rule, can_ignore_rule
from lint_utils.std import report_info
from lint_utils.text_styling import to_bold, to_cyan, to_red
from lint_utils.tree_info import TreeInfo
from lint_utils.visitors.base import BaseVisitor
from lint_utils.visitors.dto import FileInfoDTO

FuncDef: TypeAlias = ast.FunctionDef | ast.AsyncFunctionDef


@dataclass(frozen=True, slots=True, kw_only=True)
class FieldInfo:
    class_name: str
    name: str
    line: int
    col_offset: int
    assigned_to: str | None = None


class UselessFieldVisitor(BaseVisitor):
    rule: Final[str] = Rule.useless_field

    def __init__(
        self,
        file_info: FileInfoDTO,
        config: LintUtilsConfig | None = None,
    ) -> None:
        super().__init__()

        self._file_info = file_info
        self._class_name: str | None = None
        self._base_class_names: list[str] | None = None
        self._field_definitions: dict[str, FieldInfo] = {}
        self._config = config

    @property
    def useless_fields(self) -> Mapping[str, FieldInfo]:
        return self._field_definitions

    @property
    def class_name(self) -> str:
        if self._class_name:
            return self._class_name

        raise ValueError

    def _clear(self) -> None:
        self._class_name = None
        self._base_class_names = None
        self._field_definitions = {}

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        if self.can_skip_visitor:
            return

        self._class_name = node.name
        self._base_class_names = self._get_parent_class_names(node)

        if self._is_class_excluded:
            return

        for item in node.body:
            if not isinstance(item, FuncDef):
                continue

            if item.name == "__init__":
                self._process_init_assignment(item)

        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> Any:
        if isinstance(node.ctx, ast.Load):
            root_node = _find_root_node(node)
            self._field_definitions.pop(self._build_field_key(root_node.attr), None)

        return self.generic_visit(node)

    @property
    def _is_class_excluded(self) -> bool:
        if self._config is None or self._config.lint is None:
            return False

        excluded_classes = self._config.lint.exclude_classes or ()
        excluded_base_classes = self._config.lint.exclude_base_classes or ()
        all_excluded_classes = list(
            itertools.chain(excluded_classes, excluded_base_classes)
        )

        is_excluded = False
        if self._base_class_names:
            is_excluded = any(
                cls in all_excluded_classes for cls in self._base_class_names
            )

        return is_excluded or self.class_name in all_excluded_classes

    def _get_parent_class_names(self, node: ast.ClassDef) -> list[str] | None:
        base_names = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                base_names.append(base.id)

        return base_names

    def _process_init_assignment(self, method: FuncDef):
        for item in method.body:
            match item:
                case ast.Assign():
                    target = item.targets[0]
                    if not isinstance(target, ast.Attribute):
                        continue

                    field_info = FieldInfo(
                        class_name=self._class_name,
                        name=target.attr,
                        line=target.lineno,
                        col_offset=target.col_offset,
                        assigned_to=_get_assigned_to(item),
                    )

                case ast.AnnAssign():
                    target = item.target
                    if not isinstance(target, ast.Attribute):
                        continue

                    field_info = FieldInfo(
                        class_name=self._class_name,
                        name=target.attr,
                        line=target.lineno,
                        col_offset=target.col_offset,
                        assigned_to=_get_assigned_to(item),
                    )

                case _:
                    continue

            if can_ignore_rule(
                self._file_info.source_code_lines,
                line=field_info.line - 1,
                rule=self.rule,
            ):
                continue

            self._field_definitions[self._build_field_key(field_info.name)] = field_info

    def _build_field_key(self, field_name: str) -> str:
        return f"{self._class_name}_{field_name}"


def _get_assigned_to(attr: ast.Assign | ast.AnnAssign) -> str | None:
    if not isinstance(attr.value, ast.Name):
        return

    return attr.value.id


def _find_root_node(node: ast.Attribute) -> ast.Attribute:
    if isinstance(node.value, ast.Attribute):
        return _find_root_node(node.value)

    return node


def check_useless_field(
    info: TreeInfo,
    *,
    file_path: Path,
    config: LintUtilsConfig | None = None,
) -> bool:
    has_errors = []
    for module in ast.walk(info.tree):
        if isinstance(module, ast.Module):
            for item in module.body:
                if not isinstance(item, ast.ClassDef):
                    continue

                visitor = UselessFieldVisitor(
                    file_info=FileInfoDTO(
                        source_code_lines=info.raw.split("\n"),
                        path=file_path,
                    ),
                    config=config,
                )
                visitor.visit(item)

                if visitor.useless_fields:
                    msg = f"{to_bold(to_cyan(visitor.rule))} Unused object class fields found in class {to_bold(visitor.class_name)}"
                    report_info(msg)
                    for field_info in visitor.useless_fields.values():
                        full_path = f"{file_path.as_posix()}:{field_info.line}:{field_info.col_offset + 1}"
                        line_msg = (
                            f"{full_path} {to_bold(to_red(f'self.{field_info.name}'))}"
                        )
                        report_info(line_msg)
                    report_info("")

                    has_errors.append(True)

                has_errors.append(False)

    return any(has_errors)

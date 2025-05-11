from types import SimpleNamespace


class Rule(SimpleNamespace):
    useless_field = "USL001"


def can_ignore_rule(code_lines: list[str], line: int, rule: str) -> bool:
    return rule in code_lines[line]

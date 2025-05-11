from pathlib import Path
from lint_utils.config import PyProject
from lint_utils.tree_info import get_tree_info
from lint_utils.visitors.useless_fields import check_useless_field


def main() -> None:
    config = PyProject.from_toml(Path("pyproject.toml"))

    path = Path("_excluded")
    info = get_tree_info(path)
    assert info
    assert config
    assert config.tool
    assert config.tool.lint_utils
    has_useless_fields = check_useless_field(
        info,
        file_path=path,
        config=config.tool.lint_utils,
    )
    print(has_useless_fields)


if __name__ == "__main__":
    main()

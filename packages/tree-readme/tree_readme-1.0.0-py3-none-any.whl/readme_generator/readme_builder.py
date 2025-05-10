from datetime import datetime
from pathlib import Path

from readme_generator.repo_structure import walk_repo

README_TEMPLATE: str = """
# {repo_name}

## Overview
{overview}

## Folder Structure
```
{tree}
```

## Files Description
{descriptions}

## Installation

## Usage

-------------------------------------------
**Last updated on {date}**
"""


def generate_tree(root_dir: str) -> str:
    """
    Generates the folder tree structure.

    Args:
        root_dir (str): Path to the root directory.

    Returns:
        str: Formatted folder tree structure.
    """
    lines = []
    for _, line, _ in walk_repo(root_dir, tree_style=True):
        lines.append(line)
    return "\n".join(lines)


def generate_descriptions(root_dir: str) -> list[str]:
    """
    Generates file descriptions.

    Args:
        root_dir (str): Path to the root directory.

    Returns:
        list[str]: List of formatted file descriptions.
    """
    descriptions = []
    for _, line, _ in walk_repo(root_dir, tree_style=False):
        descriptions.append(line)
    return descriptions


def build_readme(repo_path: str, overview_text: str = "") -> str:
    """
    Constructs complete README.

    Args:
        repo_path (str): Path to the repository.
        overview_text (str): Overview text for the README.

    Returns:
        str: Formatted README content.
    """
    repo_name = Path(repo_path).name
    return README_TEMPLATE.format(
        repo_name=repo_name,
        overview=overview_text,
        tree=generate_tree(repo_path),
        descriptions="\n".join(generate_descriptions(repo_path)),
        date=datetime.now().strftime("%Y-%m-%d %H:%M"),
    )

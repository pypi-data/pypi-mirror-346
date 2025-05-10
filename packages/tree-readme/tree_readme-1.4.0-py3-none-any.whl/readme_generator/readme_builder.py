from datetime import datetime
import os
from readme_generator.repo_structure import walk_repo

README_TEMPLATE: str = """# {repo_name}

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


def build_readme(
    repo_path: str,
    overview_text: str = "",
    exclude_dirs: set[str] = None,
    exclude_files: set[str] = None,
) -> str:
    """
    Constructs complete README.

    Args:
        repo_path (str): Path to the repository.
        overview_text (str): Overview text for the README.
        exclude_dirs (set[str]): Directories to exclude from the folder tree.
        exclude_files (set[str]): Files to exclude from the folder tree.

    Returns:
        str: Formatted README content.
    """
    repo_name = os.path.basename(repo_path)
    return README_TEMPLATE.format(
        repo_name=repo_name,
        overview=overview_text,
        tree=generate_tree(repo_path, exclude_dirs, exclude_files),
        descriptions="\n".join(
            generate_descriptions(repo_path, exclude_dirs, exclude_files)
        ),
        date=datetime.now().strftime("%Y-%m-%d %H:%M"),
    )


def generate_tree(
    root_dir: str, exclude_dirs: set[str] = None, exclude_files: set[str] = None
) -> str:
    """
    Generates the folder tree structure.

    Args:
        root_dir (str): Path to the root directory.
        exclude_dirs (set[str]): Directories to exclude.
        exclude_files (set[str]): Files to exclude.

    Returns:
        str: Formatted folder tree structure.
    """
    lines = []
    for _, line, _ in walk_repo(
        root_dir,
        exclude_dirs=exclude_dirs,
        exclude_files=exclude_files,
        tree_style=True,
    ):
        lines.append(line)
    return "\n".join(lines)


def generate_descriptions(
    root_dir: str, exclude_dirs: set[str] = None, exclude_files: set[str] = None
) -> list[str]:
    """
    Generates file descriptions.

    Args:
        root_dir (str): Path to the root directory.
        exclude_dirs (set[str]): Directories to exclude.
        exclude_files (set[str]): Files to exclude.

    Returns:
        list[str]: List of formatted file descriptions.
    """
    descriptions = []
    for _, line, _ in walk_repo(
        root_dir,
        exclude_dirs=exclude_dirs,
        exclude_files=exclude_files,
        tree_style=False,
    ):
        descriptions.append(line)
    return descriptions

from pathlib import Path

EMOJI_MAPPING: dict[str, str] = {
    "folder": "📁",
    ".py": "🐍",
    ".ipynb": "📓",
    ".csv": "📊",
    ".json": "📋",
    ".md": "📝",
    ".txt": "📃",
    ".yaml": "⚙️",
    ".yml": "⚙️",
    ".png": "🖼️",
    ".jpg": "🖼️",
    ".gitignore": "👻",
    ".dockerfile": "🐳",
    "default": "📄",
}


def get_emoji(path: Path) -> str:
    """
    Returns emoji for file/folder.

    Args:
        path (Path): Path to the file or folder.

    Returns:
        str: Corresponding emoji.
    """
    if path.is_dir():
        return EMOJI_MAPPING["folder"]
    return EMOJI_MAPPING.get(path.suffix.lower(), EMOJI_MAPPING["default"])

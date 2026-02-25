from pathlib import Path
import re


def find_strings_files(root_path: Path, *, include_pattern: str, exclude_pattern: str) -> list[Path]:
    """
    EN: Recursively find files matching include regex and not matching exclude regex.
    ES: Buscar recursivamente ficheros que cumplan el include regex y no el exclude regex.
    """
    include_re = re.compile(include_pattern)
    exclude_re = re.compile(exclude_pattern) if exclude_pattern else None

    matched_files: list[Path] = []

    for path in root_path.rglob("*"):
        if not path.is_file():
            continue

        path_str = str(path.as_posix())

        # Skip excluded paths
        if exclude_re and exclude_re.search(path_str):
            continue

        # Skip non-included paths
        if not include_re.search(path_str):
            continue

        matched_files.append(path)

    return matched_files
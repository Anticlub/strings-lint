from pathlib import Path
import re

DEFAULT_EXCLUDE = r"(^|/)(tests|\.git|__pycache__|build|Pods|Carthage|DerivedData|SourcePackages)(/|$)"


def find_strings_files(root_path: Path, *, include_pattern: str, exclude_pattern: str) -> list[Path]:
    """
    EN: Recursively find files matching include regex and not matching exclude regex.
    ES: Buscar recursivamente ficheros que cumplan el include regex y no el exclude regex.
    """
    include_re = re.compile(include_pattern)
    
    if exclude_pattern:
        combined_exclude = f"(?:{DEFAULT_EXCLUDE})|(?:{exclude_pattern})"
    else:
        combined_exclude = DEFAULT_EXCLUDE
        
    exclude_re = re.compile(combined_exclude)

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
import argparse
from pathlib import Path
import sys
import re
import json
from strings_lint.reporter import report_issues

def main():
    errors = []
    files_with_errors = set()
    
    args = parse_args()
    root_path = Path(args.root)
    
    if not root_path.exists():
        print("Error: root path does not exist")
        sys.exit(1)

    if not root_path.is_dir():
        print("Error: root path is not a directory")
        sys.exit(1)
    
    print("Scanning root:", root_path)
    # Parse CLI arguments and scan the repository for .strings files.
    strings_files = find_strings_files(root_path, include_pattern=args.include, exclude_pattern=args.exclude)
    print(f"Found {len(strings_files)} .strings files")
    
    for file_path in strings_files:
        errors.extend(validate_file(file_path))
    
    exit_code = report_issues(errors, files_scanned=len(strings_files), fail_on=args.fail_on, output_format=args.format)
    sys.exit(exit_code)
        
def parse_args() -> argparse.Namespace:
    """
    EN: Parse command-line arguments for the validator CLI.
    ES: Parsear los argumentos de línea de comandos del CLI del validador.
    """
    parser = argparse.ArgumentParser(description="Validate .strings files")
    parser.add_argument("--root", default=".", help="Root directory to scan")
    parser.add_argument("--exclude", default="", help="EN: Regex for paths to exclude. ES: Regex de rutas a excluir.")
    parser.add_argument("--include", default=r"\.strings$", help="EN: Regex for paths to include. ES: Regex para incluir rutas.")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="EN: Output format. ES: Formato de salida.")
    parser.add_argument("--fail-on", choices=["errors", "warnings"], default="errors", help="EN: Exit with failure on errors or warnings. ES: Fallar por errores o también por avisos.")
    return parser.parse_args()

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

def validate_file(file_path: Path) -> list[dict]:
    """
    EN: Validate a single .strings file and return a list of issues (errors/warnings).
    ES: Validar un fichero .strings y devolver una lista de incidencias (errores/avisos).
    """
    issues: list[dict] = []
    inside_block_comment = False
    block_comment_start_line = None
    block_comment_start_snippet = ""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            # Validate entry structure following a strict one-entry-per-line MVP rule.
            for line_number, line in enumerate(f, start=1):
                line = line.strip()
                # Skip all lines until the end of the block comment is found.
                if inside_block_comment:
                    if "*/" in line:
                        inside_block_comment = False
                        block_comment_start_line = None
                        block_comment_start_snippet = ""
                        continue
                    
                    if line.startswith('"') and "=" in line and line.endswith(";"):
                        error = {
                            "file": str(file_path),
                            "line": line_number,
                            "code": "BLOCK_COMMENT_WITH_ENTRY",
                            "snippet": line[:80],
                            "severity": "WARNING"
                        }
                        issues.append(error)
                        
                    continue
                    
                if line == "":
                    continue
                if line.startswith("//"):
                    continue
                if line.startswith("/*"):
                    if "*/" not in line: # Enter block comment mode if the comment is not closed on the same line.
                        inside_block_comment = True
                        block_comment_start_line = line_number
                        block_comment_start_snippet = line[:80]
                    continue
                
                # Any non-empty line must be a comment or a quoted entry in this MVP.
                # EN: Any non-empty line must be a comment or a quoted entry in this MVP.
                # ES: En este MVP, cualquier línea no vacía debe ser comentario o una entrada entrecomillada.
                if not line.startswith('"'):
                    error = {
                        "file": str(file_path),
                        "line": line_number,
                        "code": "UNEXPECTED_LINE",
                        "snippet": line[:80],
                        "severity": "ERROR"
                    }
                    issues.append(error)
                    continue
                
                # A missing semicolon prevents reliable parsing of the entry.
                if not line.endswith(";"):
                    error = {
                        "file": str(file_path),
                        "line": line_number,
                        "code": "MISSING_SEMICOLON",
                        "snippet": line[:80],
                        "severity": "ERROR"
                    }
                    issues.append(error)
                    continue
                else:
                    if "=" not in line:
                        error = {
                            "file": str(file_path),
                            "line": line_number,
                            "code": "MISSING_EQUALS_SIGN",
                            "snippet": line[:80],
                            "severity": "ERROR"
                        }
                        issues.append(error)
                        continue
                    else:
                        # Split only on the first "=" to allow "=" inside values.
                        parts = line[:-1].split("=", 1) 
                        left = parts[0].strip()
                        right = parts[1].strip()
                        
                        if (not left.startswith('"')) or (not left.endswith('"')):
                            error = {
                                "file": str(file_path),
                                "line": line_number,
                                "code": "INVALID_KEY_QUOTING",
                                "snippet": line[:80],
                                "severity": "ERROR"
                            }
                            issues.append(error)
                            continue
                        if (not right.startswith('"')) or (not right.endswith('"')):
                            error = {
                                "file": str(file_path),
                                "line": line_number,
                                "code": "INVALID_VALUE_QUOTING",
                                "snippet": line[:80],
                                "severity": "ERROR"
                            }
                            issues.append(error)
                            continue
                        
                        key_inner = left[1:-1] # Remove the surrounding quotes for validation.
                        value_inner = right[1:-1] # Remove the surrounding quotes for validation.
                            
                        issues.extend(validate_escapes(key_inner, file=file_path, line_number=line_number, original_line=line, field="key"))
                        issues.extend(validate_escapes(value_inner, file=file_path, line_number=line_number, original_line=line, field="value"))
                            
            # Skip all lines until the end of the block comment is found.
            if inside_block_comment:
                error = {
                    "file": str(file_path),
                    "line": block_comment_start_line,
                    "code": "UNCLOSED_BLOCK_COMMENT",
                    "snippet": block_comment_start_snippet,
                    "severity": "ERROR"
                }
                issues.append(error)
                inside_block_comment = False
                    
    # Report non-UTF-8 files as read errors (required by the spec).
    except UnicodeDecodeError:
        error = {
            "file": str(file_path),
            "line": None,
            "code": "FILE_READ_ERROR",
            "snippet": "",
            "severity": "ERROR" 
        }
        issues.append(error)
    return issues

def validate_escapes(text: str, *, file: Path, line_number: int, original_line: str, field: str) -> list[dict]:
    """
    Validate escape sequences inside a quoted .strings key/value.

    EN: Validate escape sequences inside a quoted .strings key/value.
    ES: Validar secuencias de escape dentro de un key/value entrecomillado.
    """
    issues: list[dict] = []
    allowed = {'\\', '"', 'n', 'r', 't'}
    i = 0
    while i < len(text):
        if text[i] != '\\':
            i += 1
            continue

        # We found a backslash: validate the escape sequence.
        # EN: We found a backslash: validate the escape sequence.
        # ES: Hemos encontrado una barra invertida: validar la secuencia de escape.
        if i == len(text) - 1:
            issues.append({
                "file": str(file),
                "line": line_number,
                "code": "INCOMPLETE_ESCAPE_SEQUENCE",
                "snippet": original_line[:80],
                "severity": "ERROR",
            })
            break

        next_ch = text[i + 1]
        if next_ch not in allowed:
            issues.append({
                "file": str(file),
                "line": line_number,
                "code": "INVALID_ESCAPE_SEQUENCE",
                "snippet": original_line[:80],
                "severity": "ERROR",
            })

        i += 2
    return issues

if __name__ == "__main__":
    main()
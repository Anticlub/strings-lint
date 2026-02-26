from pathlib import Path
from typing import Optional


def validate_file(file_path: Path) -> list[dict]:
    """
    EN: Validate a single .strings file and return a list of issues (errors/warnings).
    ES: Validar un fichero .strings y devolver una lista de incidencias (errores/avisos).
    """
    issues: list[dict] = []
    seen_keys: dict[str, int] = {}
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
                        if key_inner in seen_keys:
                            error = {
                                "file": str(file_path),
                                "line": line_number,
                                "code": "DUPLICATE_KEY",
                                "snippet": line[:80],
                                "severity": "ERROR"
                            }
                            issues.append(error)
                        else:
                            seen_keys[key_inner] = line_number
                            
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

def extract_keys(file_path: Path) -> set[str]:
    """
    Extract the set of keys from a .strings file, ignoring parsing errors.

    EN: Extract the set of keys from a .strings file, ignoring parsing errors.
    ES: Extraer el conjunto de claves de un fichero .strings, ignorando errores de parseo.
    """
    keys: set[str] = set()
    inside_block_comment = False

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()

                # Handle block comments (/* ... */), including multiline.
                if inside_block_comment:
                    if "*/" in line:
                        inside_block_comment = False
                    continue

                if not line:
                    continue
                if line.startswith("//"):
                    continue
                if line.startswith("/*"):
                    # If not closed on the same line, enter block-comment mode.
                    if "*/" not in line:
                        inside_block_comment = True
                    continue

                # MVP rule: one entry per line, must be a quoted entry.
                if not (line.startswith('"') and line.endswith(";") and "=" in line):
                    continue

                # Split only on the first '=' to allow '=' inside values.
                parts = line[:-1].split("=", 1)
                left = parts[0].strip()

                # Only accept well-quoted keys.
                if left.startswith('"') and left.endswith('"'):
                    key_inner = left[1:-1]
                    keys.add(key_inner)

    except (OSError, UnicodeDecodeError):
        # Ignore read/encoding failures here; the main validator reports them.
        return set()

    return keys

def _get_locale_from_path(file_path: Path) -> Optional[str]:
    """
    EN: Extract locale code from a path containing an `xx.lproj` directory.
    ES: Extraer el código de idioma de una ruta que contenga un directorio `xx.lproj`.
    """
    for part in file_path.parts:
        if part.endswith(".lproj"):
            return part[:-len(".lproj")]
    return None

def validate_locale_consistency(files: list[Path]) -> list[dict]:
    """
    EN: Validate that localized variants of the same .strings file share the same keys.
    ES: Validar que las variantes por idioma del mismo fichero .strings tengan las mismas claves.

    Baseline rule (MVP):
    - If `en.lproj` exists for a group, use it as baseline.
    - Otherwise, use the first locale found.

    This MVP reports only missing keys (MISSING_KEY_IN_LOCALE).
    """
    issues: list[dict] = []

    # Group by base filename, then locale.
    groups: dict[str, dict[str, Path]] = {}
    for file_path in files:
        locale = _get_locale_from_path(file_path)
        if locale is None:
            continue

        base_name = file_path.name
        groups.setdefault(base_name, {})[locale] = file_path

    for base_name, locale_map in groups.items():
        if len(locale_map) < 2:
            continue

        baseline_locale = "en" if "en" in locale_map else next(iter(locale_map.keys()))
        baseline_path = locale_map[baseline_locale]
        baseline_keys = extract_keys(baseline_path)

        for locale, path in locale_map.items():
            if locale == baseline_locale:
                continue

            current_keys = extract_keys(path)
            missing = baseline_keys - current_keys

            for key in sorted(missing):
                issues.append({
                    "file": str(path),
                    "line": None,
                    "code": "MISSING_KEY_IN_LOCALE",
                    "snippet": f'"{key}"',
                    "severity": "ERROR",
                })

    return issues
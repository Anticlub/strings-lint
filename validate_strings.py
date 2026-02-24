import argparse
from pathlib import Path
import sys


def main():
    errors = []
    files_with_errors = set()
    
    parser = argparse.ArgumentParser(description="Validate .strings files")
    parser.add_argument("--root", default=".", help="Root directory to scan")
    args = parser.parse_args()
    root_path = Path(args.root)
    
    if not root_path.exists():
        print("Error: root path does not exist")
        sys.exit(1)

    if not root_path.is_dir():
        print("Error: root path is not a directory")
        sys.exit(1)
    
    print("Scanning root:", root_path)
    # Parse CLI arguments and scan the repository for .strings files.
    strings_files = list(root_path.rglob("*.strings"))
    print(f"Found {len(strings_files)} .strings files")
    
    for file in strings_files:
        inside_block_comment = False
        block_comment_start_line = None
        block_comment_start_snippet = ""
        try:
            with open(file, "r", encoding="utf-8") as f:
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
                                "file": str(file),
                                "line": line_number,
                                "code": "BLOCK_COMMENT_WITH_ENTRY",
                                "snippet": line[:80],
                                "severity": "WARNING"
                            }
                            errors.append(error)
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
                    # A missing semicolon prevents reliable parsing of the entry.
                    if not line.endswith(";"):
                        error = {
                            "file": str(file),
                            "line": line_number,
                            "code": "MISSING_SEMICOLON",
                            "snippet": line[:80],
                            "severity": "ERROR"
                        }
                        errors.append(error)
                        continue
                    else:
                        if "=" not in line:
                            error = {
                                "file": str(file),
                                "line": line_number,
                                "code": "MISSING_EQUALS_SIGN",
                                "snippet": line[:80],
                                "severity": "ERROR"
                            }
                            errors.append(error)
                            continue
                        else:
                            # Split only on the first "=" to allow "=" inside values.
                            parts = line[:-1].split("=", 1) 
                            left = parts[0].strip()
                            right = parts[1].strip()

                            if (not left.startswith('"')) or (not left.endswith('"')):
                                error = {
                                    "file": str(file),
                                    "line": line_number,
                                    "code": "INVALID_KEY_QUOTING",
                                    "snippet": line[:80],
                                    "severity": "ERROR"
                                }
                                errors.append(error)
                                continue
                            if (not right.startswith('"')) or (not right.endswith('"')):
                                error = {
                                    "file": str(file),
                                    "line": line_number,
                                    "code": "INVALID_VALUE_QUOTING",
                                    "snippet": line[:80],
                                    "severity": "ERROR"
                                }
                                errors.append(error)
                                continue

                # Skip all lines until the end of the block comment is found.
                if inside_block_comment:
                    error = {
                        "file": str(file),
                        "line": block_comment_start_line,
                        "code": "UNCLOSED_BLOCK_COMMENT",
                        "snippet": block_comment_start_snippet,
                        "severity": "ERROR"
                    }
                    errors.append(error)
                    inside_block_comment = False
                    
        # Report non-UTF-8 files as read errors (required by the spec).
        except UnicodeDecodeError:
            print(f"Encoding error in file: {file}")
    
    for error in errors:
        files_with_errors.add(error["file"])
        
    for error in errors:
        print(f"{error['severity']} {error['code']}")
        print(f"   File: {error['file']}")
        print(f"   Line: {error['line']}")
        print(f"   Snippet: {error['snippet']}")
        print(f"   Severity: {error['severity']}")
        print()
    
    error_count = sum(1 for e in errors if e["severity"] == "ERROR")
    warning_count = sum(1 for e in errors if e["severity"] == "WARNING")
    
    print("---")
    print(f"Files scanned: {len(strings_files)}")
    print(f"Error count: {error_count}")
    print(f"Warning count: {warning_count}")
    print(f"Files with errors: {len(files_with_errors)}")
    
    if error_count > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
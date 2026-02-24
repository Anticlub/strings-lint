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
        try:
            with open(file, "r", encoding="utf-8") as f:
                # Validate entry structure following a strict one-entry-per-line MVP rule.
                for line_number, line in enumerate(f, start=1):
                    line = line.strip()
                    if line == "":
                        continue
                    if line.startswith("//"):
                        continue
                    if line.startswith("/*"):
                        continue
                    # A missing semicolon prevents reliable parsing of the entry.
                    if not line.endswith(";"):
                        error = {
                            "file": str(file),
                            "line": line_number,
                            "code": "MISSING_SEMICOLON",
                            "snippet": line[:80]
                        }
                        errors.append(error)
                        continue
                    else:
                        if "=" not in line:
                            error = {
                                "file": str(file),
                                "line": line_number,
                                "code": "MISSING_EQUALS_SIGN",
                                "snippet": line[:80]
                            }
                            errors.append(error)
                            continue
                        else:
                            # Split only on the first "=" to allow "=" inside values.
                            parts = line[:-1].split("=", 1) 
                            left = parts[0].strip()
                            rigth = parts[1].strip()

                            if (not left.startswith('"')) or (not left.endswith('"')):
                                error = {
                                    "file": str(file),
                                    "line": line_number,
                                    "code": "INVALID_KEY_QUOTING",
                                    "snippet": line[:80]
                                }
                                errors.append(error)
                                continue
                            if (not rigth.startswith('"')) or (not rigth.endswith('"')):
                                error = {
                                    "file": str(file),
                                    "line": line_number,
                                    "code": "INVALID_VALUE_QUOTING",
                                    "snippet": line[:80]
                                }
                                errors.append(error)
                                continue
        
        # Report non-UTF-8 files as read errors (required by the spec).
        except UnicodeDecodeError:
            print(f"Encoding error in file: {file}")
    
    for error in errors:
        files_with_errors.add(error["file"])
        
    for error in errors:
        print(f"ERROR {error['code']}")
        print(f"   File: {error['file']}")
        print(f"   Line: {error['line']}")
        print(f"   Snippet: {error['snippet']}")
        print()
    
    print("---")
    print(f"Files scanned: {len(strings_files)}")
    print(f"Files with errors: {len(files_with_errors)}")

    
    if len(errors) > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
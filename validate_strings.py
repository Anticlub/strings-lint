import argparse
from pathlib import Path
import sys
import re
import json
from strings_lint.reporter import report_issues
from strings_lint.scanner import find_strings_files
from strings_lint.validator import validate_file

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

if __name__ == "__main__":
    main()
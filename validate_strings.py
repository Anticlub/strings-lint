import argparse
from pathlib import Path
import sys


def main():
    errors = []
    
    parser = argparse.ArgumentParser(description="Validate .strings files")
    parser.add_argument("--root", default=".", help="Root directory to scan")
    args = parser.parse_args()
    root_path = Path(args.root)
    
    if not root_path.exists():
        print("Error: root path does not exist")
        return

    if not root_path.is_dir():
        print("Error: root path is not a directory")
        return
    
    print("Scanning root:", root_path)
    
    strings_files = list(root_path.rglob("*.strings"))
    print(f"Found {len(strings_files)} .strings files")
    
    for file in strings_files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                for line_number, line in enumerate(f, start=1):
                    line = line.strip()
                    if line == "":
                        continue
                    if line.startswith("//"):
                        continue
                    if line.startswith("/*"):
                        continue
                    if not line.endswith(";"):
                        error = {
                            "file": str(file),
                            "line": line_number,
                            "code": "MISSING SEMICOLON",
                            "snipet": line[:80]
                        }
                        
                        errors.append(error)
                
        except UnicodeDecodeError:
            print(f"Encoding error in file: {file}")
            

            
    print(f"Total errors: {len(errors)}")
    print(errors)
    if len(errors) > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
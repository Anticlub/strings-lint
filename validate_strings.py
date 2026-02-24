import argparse
from pathlib import Path


def main():
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
    
    string_files = list(root_path.rglob("*.strings"))
    print(f"Found {len(string_files)} .strings files")
    
    for file in string_files:
        print("-", file)
    

if __name__ == "__main__":
    main()
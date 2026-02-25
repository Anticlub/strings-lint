from pathlib import Path
from strings_lint.scanner import find_strings_files

def test_scanner_finds_strings_files(tmp_path: Path):
    (tmp_path / "a.strings").write_text('"K"="V";\n', encoding="utf-8")
    (tmp_path / "b.txt").write_text("hello\n", encoding="utf-8")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "c.strings").write_text('"K"="V";\n', encoding="utf-8")

    files = find_strings_files(tmp_path, include_pattern=r"\.strings$", exclude_pattern="")

    paths = {p.name for p in files}
    assert paths == {"a.strings", "c.strings"}
    
def test_scanner_excludes_paths(tmp_path: Path):
        (tmp_path / "keep.strings").write_text('"K"="V";\n', encoding="utf-8")
        (tmp_path / "Pods").mkdir()
        (tmp_path / "Pods" / "ignored.strings").write_text('"K"="V";\n', encoding="utf-8")

        files = find_strings_files(tmp_path, include_pattern=r"\.strings$", exclude_pattern=r"Pods")

        names = {p.name for p in files}
        assert names == {"keep.strings"}

def test_scanner_include_filters(tmp_path: Path):
    (tmp_path / "Localizable.strings").write_text('"K"="V";\n', encoding="utf-8")
    (tmp_path / "Other.strings").write_text('"K"="V";\n', encoding="utf-8")

    files = find_strings_files(tmp_path, include_pattern=r"Localizable\.strings$", exclude_pattern="")

    names = {p.name for p in files}
    assert names == {"Localizable.strings"}    
from pathlib import Path
from validate_strings import validate_file
from strings_lint.reporter import report_issues

def test_valid_file_has_no_issues():
    fixture = Path("tests/fixtures/valid.strings")
    issues = validate_file(fixture)
    assert issues == []
    
def test_missing_semicolon_is_reported():
    fixture = Path(__file__).parent / "fixtures" / "missing_semicolon.strings"
    issues = validate_file(fixture)

    # Queremos al menos 1 issue con ese code
    assert any(i["code"] == "MISSING_SEMICOLON" for i in issues)
    
def test_invalid_escape_sequence_is_reported():
    fixture = Path(__file__).parent / "fixtures" / "invalid_escape.strings"
    issues = validate_file(fixture)

    assert any(i["code"] == "INVALID_ESCAPE_SEQUENCE" for i in issues)
    
def test_incomplete_escape_sequence_is_reported():
    fixture = Path(__file__).parent / "fixtures" / "incomplete_escape.strings"
    issues = validate_file(fixture)

    assert any(i["code"] == "INCOMPLETE_ESCAPE_SEQUENCE" for i in issues)
    
def test_unclosed_block_comment_is_reported():
    fixture = Path(__file__).parent / "fixtures" / "unclosed_block_comment.strings"
    issues = validate_file(fixture)

    assert any(i["code"] == "UNCLOSED_BLOCK_COMMENT" for i in issues)
    



def test_report_no_issues_returns_zero(capsys):
    exit_code = report_issues(
        issues=[],
        files_scanned=1,
        fail_on="errors",
        output_format="text"
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Total errors: 0" in captured.out
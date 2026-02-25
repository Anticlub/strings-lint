from strings_lint.reporter import report_issues
import json

def test_reporter_no_issues_returns_zero(capsys):
    exit_code = report_issues(
        issues=[],
        files_scanned=2,
        fail_on="errors",
        output_format="text",
    )

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Files scanned: 2" in captured.out
    assert "Total errors: 0" in captured.out
    assert "Total warnings: 0" in captured.out
    
def test_reporter_warning_does_not_fail_when_fail_on_errors(capsys):
    issues = [
        {
            "file": "a.strings",
            "line": 1,
            "code": "W1",
            "snippet": "x",
            "severity": "WARNING",
        }
    ]

    exit_code = report_issues(
        issues=issues,
        files_scanned=1,
        fail_on="errors",
        output_format="text",
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Total warnings: 1" in captured.out
    
def test_reporter_warning_fails_when_fail_on_warnings(capsys):
    issues = [
        {
            "file": "a.strings",
            "line": 1,
            "code": "W1",
            "snippet": "x",
            "severity": "WARNING",
        }
    ]

    exit_code = report_issues(
        issues=issues,
        files_scanned=1,
        fail_on="warnings",
        output_format="text",
    )

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Total errors: 0" in captured.out
    assert "Total warnings: 1" in captured.out
    

def test_reporter_outputs_valid_json(capsys):
    issues = [
        {
            "file": "a.strings",
            "line": 2,
            "code": "E1",
            "snippet": "bad",
            "severity": "ERROR",
        }
    ]

    exit_code = report_issues(
        issues=issues,
        files_scanned=1,
        fail_on="errors",
        output_format="json",
    )

    out = capsys.readouterr().out
    data = json.loads(out)

    assert data["summary"]["files_scanned"] == 1
    assert data["summary"]["total_errors"] == 1
    assert exit_code == 1

def test_reporter_error_in_text_is_printed_and_counted(capsys):
    issues = [
        {
            "file": "a.strings",
            "line": 10,
            "code": "E1",
            "snippet": "bad stuff",
            "severity": "ERROR",
        }
    ]

    exit_code = report_issues(
        issues=issues,
        files_scanned=1,
        fail_on="errors",
        output_format="text",
    )

    out = capsys.readouterr().out

    assert exit_code == 1
    assert "ERROR E1" in out
    assert "Total errors: 1" in out
    assert "Total warnings: 0" in out
    
def test_reporter_outputs_json_with_warning_count(capsys):
    issues = [
        {
            "file": "a.strings",
            "line": 1,
            "code": "W1",
            "snippet": "x",
            "severity": "WARNING",
        }
    ]

    exit_code = report_issues(
        issues=issues,
        files_scanned=1,
        fail_on="errors",
        output_format="json",
    )

    out = capsys.readouterr().out
    data = json.loads(out)

    assert exit_code == 0
    assert data["summary"]["total_errors"] == 0
    assert data["summary"]["total_warnings"] == 1
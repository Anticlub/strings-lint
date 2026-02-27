from pathlib import Path
from strings_lint.validator import (
    validate_missing_keys,
    validate_placeholder_consistency,
)


# -----------------------
# MISSING KEY TESTS
# -----------------------

def test_missing_key_detected():
    baseline = {
        "hello": {"value": "Hello", "line": 10},
        "bye": {"value": "Bye", "line": 11},
    }

    current = {
        "hello": {"value": "Hola", "line": 20},
    }

    issues = validate_missing_keys(
        baseline,
        current,
        file_path=Path("es.lproj/Localizable.strings"),
    )

    assert len(issues) == 1
    assert issues[0]["code"] == "MISSING_KEY_IN_LOCALE"
    assert '"bye"' in issues[0]["snippet"]
    # Missing keys report the baseline line (where the key is defined in baseline)
    assert issues[0]["line"] == 11


def test_no_missing_keys():
    baseline = {
        "hello": {"value": "Hello", "line": 10},
    }

    current = {
        "hello": {"value": "Hola", "line": 20},
    }

    issues = validate_missing_keys(
        baseline,
        current,
        file_path=Path("es.lproj/Localizable.strings"),
    )

    assert issues == []


# -----------------------
# PLACEHOLDER TESTS
# -----------------------

def test_placeholder_mismatch_detected():
    baseline = {
        "greeting": {"value": "Hello %@", "line": 10},
    }

    current = {
        "greeting": {"value": "Hola", "line": 20},
    }

    issues = validate_placeholder_consistency(
        baseline,
        current,
        file_path=Path("es.lproj/Localizable.strings"),
    )

    assert len(issues) == 1
    assert issues[0]["code"] == "PLACEHOLDER_MISMATCH"
    # Placeholder mismatch reports current locale line
    assert issues[0]["line"] == 20


def test_placeholder_match_ok():
    baseline = {
        "greeting": {"value": "Hello %@", "line": 10},
    }

    current = {
        "greeting": {"value": "Hola %@", "line": 20},
    }

    issues = validate_placeholder_consistency(
        baseline,
        current,
        file_path=Path("es.lproj/Localizable.strings"),
    )

    assert issues == []


def test_double_percent_not_counted_as_placeholder():
    baseline = {
        "progress": {"value": "Progress 50%%", "line": 10},
    }

    current = {
        "progress": {"value": "Progreso 50%%", "line": 20},
    }

    issues = validate_placeholder_consistency(
        baseline,
        current,
        file_path=Path("es.lproj/Localizable.strings"),
    )

    assert issues == []
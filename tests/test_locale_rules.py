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
        "hello": "Hello",
        "bye": "Bye",
    }

    current = {
        "hello": "Hola",
    }

    issues = validate_missing_keys(
        baseline,
        current,
        file_path=Path("es.lproj/Localizable.strings"),
    )

    assert len(issues) == 1
    assert issues[0]["code"] == "MISSING_KEY_IN_LOCALE"
    assert '"bye"' in issues[0]["snippet"]


def test_no_missing_keys():
    baseline = {
        "hello": "Hello",
    }

    current = {
        "hello": "Hola",
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
        "greeting": "Hello %@",
    }

    current = {
        "greeting": "Hola",
    }

    issues = validate_placeholder_consistency(
        baseline,
        current,
        file_path=Path("es.lproj/Localizable.strings"),
    )

    assert len(issues) == 1
    assert issues[0]["code"] == "PLACEHOLDER_MISMATCH"


def test_placeholder_match_ok():
    baseline = {
        "greeting": "Hello %@",
    }

    current = {
        "greeting": "Hola %@",
    }

    issues = validate_placeholder_consistency(
        baseline,
        current,
        file_path=Path("es.lproj/Localizable.strings"),
    )

    assert issues == []


def test_double_percent_not_counted_as_placeholder():
    baseline = {
        "progress": "Progress 50%%",
    }

    current = {
        "progress": "Progreso 50%%",
    }

    issues = validate_placeholder_consistency(
        baseline,
        current,
        file_path=Path("es.lproj/Localizable.strings"),
    )

    assert issues == []
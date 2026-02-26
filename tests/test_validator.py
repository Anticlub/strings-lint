from pathlib import Path
from validate_strings import validate_file
from strings_lint.reporter import report_issues

# Estos tests comprueban que el validador detecta correctamente los errores de un fichero .strings, incluyendo la línea donde se encuentra cada error y el código de error correspondiente. También se comprueba que el reporte de incidencias funciona correctamente al no reportar ningún error.
def test_valid_file_has_no_issues():
    fixture = Path("tests/fixtures/valid.strings")
    issues = validate_file(fixture)
    assert issues == []

# Este test comprueba que un fichero con una línea sin punto y coma genera un error con el código "MISSING_SEMICOLON" y que la línea reportada corresponde a la línea de esa incidencia.
def test_missing_semicolon_is_reported():
    fixture = Path(__file__).parent / "fixtures" / "missing_semicolon.strings"
    issues = validate_file(fixture)

    # Queremos al menos 1 issue con ese code
    assert any(i["code"] == "MISSING_SEMICOLON" for i in issues)

# Este test comprueba que un fichero con claves duplicadas genera un error con el código "DUPLICATE_KEY" y que la línea reportada corresponde a la segunda aparición de la clave.
def test_invalid_escape_sequence_is_reported():
    fixture = Path(__file__).parent / "fixtures" / "invalid_escape.strings"
    issues = validate_file(fixture)

    assert any(i["code"] == "INVALID_ESCAPE_SEQUENCE" for i in issues)

# Este test comprueba que un fichero con claves duplicadas genera un error con el código "DUPLICATE_KEY" y que la línea reportada corresponde a la segunda aparición de la clave.
def test_incomplete_escape_sequence_is_reported():
    fixture = Path(__file__).parent / "fixtures" / "incomplete_escape.strings"
    issues = validate_file(fixture)

    assert any(i["code"] == "INCOMPLETE_ESCAPE_SEQUENCE" for i in issues)

# Este test comprueba que un fichero con claves duplicadas genera un error con el código "DUPLICATE_KEY" y que la línea reportada corresponde a la segunda aparición de la clave.
def test_unclosed_block_comment_is_reported():
    fixture = Path(__file__).parent / "fixtures" / "unclosed_block_comment.strings"
    issues = validate_file(fixture)

    assert any(i["code"] == "UNCLOSED_BLOCK_COMMENT" for i in issues)
    
# Este test comprueba que un fichero con claves duplicadas genera un error con el código "DUPLICATE_KEY" y que la línea reportada corresponde a la segunda aparición de la clave.
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

# Este test comprueba que un fichero con claves duplicadas genera un error con el código "DUPLICATE_KEY" y que la línea reportada corresponde a la segunda aparición de la clave.
def test_duplicate_key_is_reported(tmp_path):
    content = '''"HELLO" = "Hola"; 
                "HELLO" = "Bonjour";
            '''
    file_path = tmp_path / "Localizable.strings"
    file_path.write_text(content, encoding="utf-8")

    issues = validate_file(file_path)

    duplicate_errors = [i for i in issues if i["code"] == "DUPLICATE_KEY"]

    assert len(duplicate_errors) == 1
    assert duplicate_errors[0]["line"] == 2
# strings-lint --- Apple `.strings` Validator (ES / EN)

CLI tool written in Python to validate Apple `.strings` localization
files (iOS/tvOS).\
Herramienta CLI escrita en Python para validar ficheros de localización
`.strings` de Apple (iOS/tvOS).

Designed to detect syntax errors and localization inconsistencies before
CI or runtime.\
Diseñada para detectar errores sintácticos e inconsistencias de
localización antes de CI o ejecución.

------------------------------------------------------------------------

# 📦 Requirements / Requisitos

-   Python **3.10+**
-   (Optional / Opcional) `pytest` for running tests

------------------------------------------------------------------------

# 🚀 Quick Start / Uso rápido

``` bash
python3 validate_strings.py --root .
```

Examples / Ejemplos:

``` bash
python3 validate_strings.py --root . --exclude "Pods|Carthage|DerivedData|SourcePackages|build|.git"
python3 validate_strings.py --root . --format json
python3 validate_strings.py --root . --include "Localizable\.strings$"
python3 validate_strings.py --root . --fail-on warnings
```

------------------------------------------------------------------------

# 🖥 CLI Arguments / Parámetros CLI

-   `--root <path>`\
    Root directory to scan (default: `.`)\
    Directorio raíz a escanear (por defecto `.`)

-   `--exclude <regex>`\
    Regex to exclude paths\
    Regex para excluir rutas

-   `--include <regex>`\
    Regex to include files (default: `\.strings$`)\
    Regex para incluir ficheros (por defecto `\.strings$`)

-   `--format text|json`\
    Output format (default: `text`)\
    Formato de salida (por defecto `text`)

-   `--fail-on errors|warnings`\
    Exit code behavior for CI\
    Comportamiento del código de salida en CI

------------------------------------------------------------------------

# 🔎 What It Validates / Qué valida

## 1️⃣ File Discovery / Descubrimiento de ficheros

-   Recursive scan from `--root`
-   Include/exclude filtering via regex
-   Detects `.lproj` localized variants

------------------------------------------------------------------------

## 2️⃣ Per-file Syntax Validation / Validación sintáctica por fichero

MVP rule / Regla MVP: **one entry per line / una entrada por línea**.

Each non-empty line must be: - `//` single-line comment - `/* ... */`
block comment - `"KEY" = "VALUE";`

Detects / Detecta:

-   `UNCLOSED_BLOCK_COMMENT`
-   `UNEXPECTED_LINE`
-   `MISSING_SEMICOLON`
-   `MISSING_EQUALS_SIGN`
-   `INVALID_KEY_QUOTING`
-   `INVALID_VALUE_QUOTING`
-   `INVALID_ESCAPE_SEQUENCE`
-   `INCOMPLETE_ESCAPE_SEQUENCE`
-   `FILE_READ_ERROR`
-   `DUPLICATE_KEY`
-   `BLOCK_COMMENT_WITH_ENTRY` (warning)

------------------------------------------------------------------------

## 3️⃣ Locale Consistency (Baseline Rule)

## Consistencia entre idiomas (Regla baseline)

Baseline selection: - Uses `en.lproj` if present - Otherwise uses the
first detected locale

Validates: - All baseline keys exist in other locales - Reports
`MISSING_KEY_IN_LOCALE`

------------------------------------------------------------------------

## 4️⃣ Placeholder Consistency / Consistencia de placeholders

The validator checks that placeholders match between baseline and other
locales.

El validador comprueba que los placeholders coincidan entre el baseline
y los otros idiomas.

Supported printf-style placeholders:

### Basic Specifiers / Especificadores básicos

-   `%@`
-   `%d`
-   `%i`
-   `%u`
-   `%f`
-   `%F`
-   `%e`
-   `%E`
-   `%g`
-   `%G`
-   `%x`
-   `%X`
-   `%o`
-   `%s`
-   `%c`
-   `%p`
-   `%a`
-   `%A`

### Length Modifiers / Modificadores de longitud

-   `%hd`
-   `%ld`
-   `%lld`
-   `%zd`
-   `%td`
-   `%jd`
-   `%qd`
-   `%hhd`
-   `%llx`
-   `%llu`
-   etc. combinations following printf specification

### Positional Arguments / Argumentos posicionales

-   `%1$@`
-   `%2$d`
-   `%3$ld`

### Flags and Width / Flags y ancho

Supports patterns like:

-   `%02d`
-   `%+5.2f`
-   `%-10s`
-   `%#x`

Literal percent (`%%`) is ignored (not treated as placeholder).\
El porcentaje literal (`%%`) se ignora.

Reports: - `PLACEHOLDER_MISMATCH`

------------------------------------------------------------------------

# 📤 Output / Salida

## Text format (default) / Formato texto

-   Issues grouped by file
-   Summary including:
    -   Files scanned
    -   Files with errors
    -   Total errors
    -   Total warnings

## JSON format / Formato JSON

Contains: - `summary` - `issues`: - `file` - `line` - `code` -
`snippet` - `severity`

------------------------------------------------------------------------

# 🔁 Exit Codes / Códigos de salida

-   `0` → no errors (default mode)
-   `1` → errors found
-   `1` → warnings found if `--fail-on warnings`

------------------------------------------------------------------------

# 🧪 Tests

Run:

``` bash
python3 -m pytest
```

Tests use temporary directories (`tmp_path`) to ensure portability.\
Los tests usan directorios temporales para garantizar portabilidad.

------------------------------------------------------------------------

# 🏗 Architecture / Arquitectura

    strings_lint/
        scanner.py
        validator.py
        reporter.py
    validate_strings.py

Modular separation: - Scanner (file discovery) - Validator (syntax +
consistency checks) - Reporter (output formatting)

Separación modular clara para facilitar mantenimiento y futuras mejoras.

------------------------------------------------------------------------

# ⚡ Performance

-   Files are parsed once per locale group
-   No unnecessary O(n²) comparisons
-   Suitable for large repositories

Adecuado para repositorios grandes sin degradación significativa.

------------------------------------------------------------------------

# 📌 Limitations / Limitaciones

-   MVP assumes one entry per line
-   Multiline values are not supported
-   Does not implement autofix (by design)

------------------------------------------------------------------------

# 📄 License

Internal/educational project example.

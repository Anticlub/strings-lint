# strings-lint

CLI tool in Python to validate Apple `.strings` localization files
(iOS/tvOS).\
Herramienta CLI en Python para validar ficheros de localización
`.strings` (iOS/tvOS).

------------------------------------------------------------------------

# 📚 Overview / Descripción general

**EN:**\
This tool scans a repository, finds `.strings` files, validates their
syntax, and performs cross-locale consistency checks (missing keys and
placeholder mismatches). It is designed to be used locally or integrated
into CI pipelines.

**ES:**\
Esta herramienta analiza un repositorio, localiza ficheros `.strings`,
valida su sintaxis y realiza comprobaciones de consistencia entre
idiomas (claves faltantes y discrepancias en placeholders). Está
diseñada para uso local o integración en CI.

------------------------------------------------------------------------

# 🚀 Installation / Instalación

**EN:** Requires Python 3.10+. No heavy dependencies.

**ES:** Requiere Python 3.10+. No tiene dependencias pesadas.

``` bash
git clone <repo>
cd strings-lint
python3 validate_strings.py --root .
```

------------------------------------------------------------------------

# 🖥 CLI Usage / Uso por línea de comandos

``` bash
python validate_strings.py --root .
python validate_strings.py --root . --format json
python validate_strings.py --root . --exclude "Pods|Carthage|DerivedData|SourcePackages"
```

## Parameters / Parámetros

  ---------------------------------------------------------------------------------
  Parameter                     EN Description            ES Descripción
  ----------------------------- ------------------------- -------------------------
  `--root <path>`               Root directory to scan    Directorio raíz a
                                (default `.`)             escanear (por defecto
                                                          `.`)

  `--exclude <regex>`           Regex for excluding paths Regex para excluir rutas

  `--include <regex>`           Regex to filter files     Regex para filtrar
                                (default `\.strings$`)    ficheros

  `--format text|json`          Output format             Formato de salida

  `--fail-on warnings|errors`   Exit behavior             Comportamiento del código
                                                          de salida
  ---------------------------------------------------------------------------------

------------------------------------------------------------------------

# 🔍 What Is Validated / Qué se valida

## 1️⃣ Syntax Validation / Validación sintáctica

**EN:** Detects basic format errors in `.strings` files.\
**ES:** Detecta errores básicos de formato en ficheros `.strings`.

### Checks performed / Comprobaciones realizadas

-   Missing semicolons (`;`)
-   Unbalanced quotes (`"`)
-   Invalid escape sequences (`\`)
-   Unexpected lines
-   Unclosed block comments (`/* ... */`)
-   Duplicate keys inside the same file

### Example / Ejemplo

``` strings
"HELLO" = "Hola"
```

Output / Salida:

``` json
{
  "file": "es.lproj/Localizable.strings",
  "line": 12,
  "code": "MISSING_SEMICOLON",
  "snippet": "\"HELLO\" = \"Hola\"",
  "severity": "ERROR"
}
```

------------------------------------------------------------------------

## 2️⃣ Locale Consistency / Consistencia entre idiomas

**EN:** When multiple `.lproj` variants exist (e.g., `en.lproj`,
`es.lproj`), cross-locale validation is performed.\
**ES:** Cuando existen varias variantes `.lproj` (por ejemplo
`en.lproj`, `es.lproj`), se valida la consistencia entre idiomas.

------------------------------------------------------------------------

### 🔑 Missing Keys / Claves faltantes

**EN:** If a key exists in the baseline (`en.lproj`) but is missing in
another locale, it is reported.

**ES:** Si una clave existe en el baseline (`en.lproj`) pero falta en
otro idioma, se reporta.

``` json
{
  "file": "es.lproj/Localizable.strings",
  "line": 87,
  "code": "MISSING_KEY_IN_LOCALE",
  "snippet": "\"PROFILE_TITLE\"",
  "severity": "ERROR"
}
```

**Line reporting strategy / Estrategia de línea:**\
- EN: The reported line corresponds to where the key is defined in the
baseline file.\
- ES: La línea reportada corresponde a donde está definida la clave en
el fichero baseline.

------------------------------------------------------------------------

### 🧩 Placeholder Consistency / Consistencia de placeholders

**EN:** Ensures placeholder types and counts match across locales.\
**ES:** Asegura que el tipo y número de placeholders coincidan entre
idiomas.

Supported placeholders / Placeholders soportados:

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
-   Length modifiers: `hh`, `h`, `l`, `ll`, `q`, `z`, `t`, `j`
-   Positional arguments: `%1$@`, `%2$d`, etc.

### Example / Ejemplo

Baseline:

``` strings
"WELCOME" = "Welcome %@, you have %d messages";
```

Incorrect Spanish:

``` strings
"WELCOME" = "Bienvenido %@";
```

Output:

``` json
{
  "file": "es.lproj/Localizable.strings",
  "line": 142,
  "code": "PLACEHOLDER_MISMATCH",
  "snippet": "\"WELCOME\" baseline=['%@', '%d'] current=['%@']",
  "severity": "ERROR"
}
```

**Line reporting strategy / Estrategia de línea:**\
- EN: The reported line corresponds to the inconsistent locale file.\
- ES: La línea reportada corresponde al fichero del idioma
inconsistente.

------------------------------------------------------------------------

# 📐 Line Reporting Design / Diseño del reporte de líneas

**EN:**\
- Syntax errors → report actual file line.\
- Placeholder mismatches → report current locale line.\
- Missing keys → report baseline definition line.

**ES:**\
- Errores sintácticos → reportan la línea real del fichero.\
- Desajustes de placeholders → reportan la línea del locale actual.\
- Claves faltantes → reportan la línea donde la clave está definida en
el baseline.

This improves traceability without extra file reads.\
Esto mejora la trazabilidad sin lecturas adicionales de fichero.

------------------------------------------------------------------------

# 🧪 Tests / Tests

**EN:** Includes fixtures for valid files, syntax errors, missing keys,
and placeholder mismatches.\
**ES:** Incluye fixtures para ficheros válidos, errores sintácticos,
claves faltantes y errores de placeholders.

Run tests / Ejecutar tests:

``` bash
pytest
```

------------------------------------------------------------------------

# 🏁 Exit Codes / Códigos de salida

  Code   EN Meaning        ES Significado
  ------ ----------------- -----------------------
  0      No errors         Sin errores
  1      Errors detected   Se detectaron errores

------------------------------------------------------------------------

# 🎯 Design Philosophy / Filosofía de diseño

**EN:**\
- Single file read per locale (cached entries)\
- Lightweight parsing\
- CI-friendly structured output\
- Clear and explicit MVP constraints

**ES:**\
- Una sola lectura por fichero (caché de entradas)\
- Parseo ligero\
- Salida estructurada compatible con CI\
- Restricciones MVP explícitas

------------------------------------------------------------------------

# 📄 License / Licencia

Internal tooling / Herramienta interna.

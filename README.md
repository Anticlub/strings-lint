# strings-lint

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![CI Ready](https://img.shields.io/badge/CI-ready-success)
![License](https://img.shields.io/badge/license-internal-lightgrey)

CLI tool in Python to validate Apple `.strings` localization files (iOS/tvOS).  
Herramienta CLI en Python para validar ficheros de localización `.strings` (iOS/tvOS).

---

# 📚 Overview / Descripción general

**EN:**  
This tool scans a repository, finds `.strings` files, validates their syntax,
and performs cross-locale consistency checks (missing keys and placeholder mismatches).
It is designed to be used locally or integrated into CI pipelines.

**ES:**  
Esta herramienta analiza un repositorio, localiza ficheros `.strings`,
valida su sintaxis y realiza comprobaciones de consistencia entre idiomas
(claves faltantes y discrepancias en placeholders).
Está diseñada para uso local o integración en CI.

---

# 🚀 Installation / Instalación

**EN:** Requires Python 3.10+.  
**ES:** Requiere Python 3.10+.

```bash
git clone <repo>
cd strings-lint
python3 validate_strings.py
```

---

# 🖥 CLI Usage / Uso por línea de comandos

## Default behavior / Comportamiento por defecto

```bash
python validate_strings.py
```

**EN:** Scans the current directory (`.`) by default.  
By default, the following directories are excluded:  
`tests`, `.git`, `__pycache__`, `build`, `Pods`, `Carthage`, `DerivedData`, `SourcePackages`.

**ES:** Escanea el directorio actual (`.`) por defecto.  
Por defecto, se excluyen los siguientes directorios:  
`tests`, `.git`, `__pycache__`, `build`, `Pods`, `Carthage`, `DerivedData`, `SourcePackages`.

---

## Custom root directory / Directorio raíz personalizado

```bash
python validate_strings.py --root <path>
```

---

## JSON output / Salida en formato JSON

```bash
python validate_strings.py --format json
```

---

# 🔍 What Is Validated / Qué se valida

## 1️⃣ Syntax Validation / Validación sintáctica

- Missing semicolons (`;`)
- Unbalanced quotes (`"`)
- Invalid escape sequences (`\`)
- Unexpected lines
- Unclosed block comments (`/* ... */`)
- Duplicate keys inside the same file

---

## 2️⃣ Locale Consistency / Consistencia entre idiomas

### 🔑 Missing Keys / Claves faltantes

- EN: Missing keys are detected relative to a baseline (`en.lproj` if present).
- ES: Las claves faltantes se detectan respecto a un baseline (`en.lproj` si existe).

### 🧩 Placeholder Consistency / Consistencia de placeholders

Supported placeholders:

`%@ %d %i %u %f %F %e %E %g %G %x %X %o %s %c %p %a %A`  
Length modifiers: `hh h l ll q z t j`  
Positional arguments: `%1$@`, `%2$d`, etc.

---

# 🧪 Tests / Tests

## 🔹 Recommended Setup (Virtual Environment) / Configuración recomendada (Entorno virtual)

**EN:**  
It is recommended to run tests inside a virtual environment to avoid dependency conflicts.

**ES:**  
Se recomienda ejecutar los tests dentro de un entorno virtual para evitar conflictos de dependencias.

```bash
# Create virtual environment
python3 -m venv .venv

# Activate it (macOS / Linux)
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install test dependencies
pip install pytest

# Run tests
pytest
```

---

## 🔹 Alternative (Without activation) / Alternativa (Sin activar entorno)

```bash
python3 -m pytest
```

This ensures the correct interpreter is used.  
Esto garantiza que se use el intérprete correcto.

---

## 💡 Why virtual environments? / ¿Por qué usar entornos virtuales?

**EN:**  
Using a virtual environment prevents conflicts with globally installed Python packages
and ensures reproducible test execution.

**ES:**  
Usar un entorno virtual evita conflictos con paquetes instalados globalmente
y garantiza una ejecución reproducible de los tests.

---

# 🏁 Exit Codes / Códigos de salida

| Code | EN Meaning        | ES Significado        |
|------|------------------|-----------------------|
| 0    | No errors        | Sin errores           |
| 1    | Errors detected  | Se detectaron errores |

---

# 📄 License / Licencia

Internal tooling / Herramienta interna.

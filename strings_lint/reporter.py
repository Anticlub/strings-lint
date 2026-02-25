def report_issues(issues: list[dict], *, files_scanned: int, fail_on: str, output_format: str) -> int:
    """
    EN: Print a human-readable report and return the process exit code.
    ES: Imprimir un reporte legible y devolver el código de salida del proceso.
    """
    issues_by_file: dict[str, list[dict]] = {}
    for issue in issues:
        issues_by_file.setdefault(issue["file"], []).append(issue)
        
    for file_path in sorted(issues_by_file.keys()):
        file_issues = issues_by_file[file_path]
        print(f"\n{file_path}")
        print("-" * len(file_path))

        for issue in file_issues:
            line = issue.get("line")
            line_str = str(line) if line is not None else "-"
            print(f"{issue['severity']} {issue['code']} (line {line_str})")
            print(f"  {issue['snippet']}")
    
    error_count = sum(1 for i in issues if i["severity"] == "ERROR")
    warning_count = sum(1 for i in issues if i["severity"] == "WARNING")

    files_with_errors = {i["file"] for i in issues if i["severity"] == "ERROR"}

    summary = {
    "files_scanned": files_scanned,
    "files_with_errors": len(files_with_errors),
    "error_count": error_count,
    "warning_count": warning_count,
    }
    
    if output_format == "json":
        payload = {
            **summary,
            "issues": issues,
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        if fail_on == "warnings":
            return 1 if (error_count > 0 or warning_count > 0) else 0

        # default: fail only on errors
        return 1 if error_count > 0 else 0
    
    print("\n---")
    print(f"Files scanned: {files_scanned}")
    print(f"Files with errors: {len(files_with_errors)}")
    print(f"Total errors: {error_count}")
    print(f"Total warnings: {warning_count}")

    if fail_on == "warnings":
        return 1 if (error_count > 0 or warning_count > 0) else 0

    # default: fail only on errors
    return 1 if error_count > 0 else 0
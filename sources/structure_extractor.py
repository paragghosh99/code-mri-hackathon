from .file_parser import extract_python_imports


def analyze_file(file_path: str):

    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    imports = extract_python_imports(code)

    return {
        "file": file_path,
        "imports": imports,
        "lines": len(code.split("\n"))
    }

def analyze_code(code: str, path: str):

    imports = extract_python_imports(code)

    return {
        "file": path,
        "imports": imports,
        "lines": len(code.split("\n"))
    }
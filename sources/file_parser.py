import re


def extract_python_imports(code: str):

    imports = []

    # import x
    pattern1 = r'^import\s+([\w\.]+)'

    # from x import y
    pattern2 = r'^from\s+([\w\.]+)\s+import'

    

    for line in code.split("\n"):

        match1 = re.match(pattern1, line)
        match2 = re.match(pattern2, line)

        if match1:
            imports.append(match1.group(1))

        if match2:
            imports.append(match2.group(1))

    return list(set(imports))
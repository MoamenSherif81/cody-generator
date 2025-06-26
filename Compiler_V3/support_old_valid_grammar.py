import re


def _support_old_valid_grammar(code: str) -> str:
    code = code.strip()
    pattern = r'^row\s*\{(?:[^{}]*|\{[^{}]*\})*\}(?:\s*,\s*row\s*\{(?:[^{}]*|\{[^{}]*\})*\})*$'
    is_match = bool(re.fullmatch(pattern, code))
    if not is_match:
        code = code
    else:
        code = f"body {'{'}\n{code}\n {"}"}"
    code = code.replace("select-box", "select_box")
    return code

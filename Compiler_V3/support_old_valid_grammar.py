import re


def _support_old_valid_grammar(code: str) -> str:
    pattern = r'^(row\s*\{\s*.*?\s*\}\s*(,\s*row\s*\{\s*.*?\s*\}\s*)*)?$'
    is_match = bool(re.fullmatch(pattern, code))
    if not is_match:
        code = code
    else:
        code = f"body {'{'}\n{code}\n {"}"}"
    code = code.replace("select-box", "select_box")
    return code


print(_support_old_valid_grammar("row{},row{box{}}"))

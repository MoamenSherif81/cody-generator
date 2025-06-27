from typing import Optional

from google.api_core.exceptions import BadRequest

from Compiler_V3 import validate_dsl, compile_to_web
from Compiler_V3.support_old_valid_grammar import _support_old_valid_grammar


def safe_compile_to_web(dsl_content: Optional[str]):
    dsl_content = dsl_content.strip()
    dsl_content = _support_old_valid_grammar(dsl_content)
    is_valid, error = validate_dsl(dsl_code=dsl_content)
    if not is_valid:
        raise BadRequest(message=error)
    html, css, error = compile_to_web(dsl_content)
    return html, css

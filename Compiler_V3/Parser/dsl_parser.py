import os
from typing import Tuple, Optional

from lark import Lark, UnexpectedInput, UnexpectedToken, UnexpectedCharacters

from Compiler_V3.Parser.transformer import DSLTransformer

GRAMMAR_FILE = os.path.join(os.path.dirname(__file__), "dsl_grammar.lark")
with open(GRAMMAR_FILE, "r", encoding="utf-8") as f:
    GRAMMAR = f.read()
parser = Lark(GRAMMAR, parser="lalr", start="start")


def validate_dsl(dsl_code: str) -> tuple[bool, str | None]:
    if not dsl_code.strip():
        return False, "DSL is empty or contains only whitespace."
    try:
        parser.parse(dsl_code)
        return True, None
    except (UnexpectedInput, UnexpectedToken, UnexpectedCharacters) as e:
        return False, f"Syntax error at line {e.line}, column {e.column}:\n{e.get_context(dsl_code)}"

def generate_ast(dsl_code: str) -> dict:
    tree = parser.parse(dsl_code)
    ast = DSLTransformer().transform(tree)
    return ast


def validate_and_generate_ast(dsl_code: str) -> Tuple[bool, Optional[dict], Optional[str]]:
    if not dsl_code.strip():
        return False, None, "DSL is empty or whitespace."

    try:
        tree = parser.parse(dsl_code)
        ast = DSLTransformer().transform(tree)
        return True, ast, None
    except (UnexpectedInput, UnexpectedToken, UnexpectedCharacters) as e:
        error_msg = f"Syntax error at line {e.line}, column {e.column}:\n{e.get_context(dsl_code)}"
        return False, None, error_msg
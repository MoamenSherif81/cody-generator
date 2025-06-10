import os

from lark import Lark, UnexpectedInput, UnexpectedToken, UnexpectedCharacters

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

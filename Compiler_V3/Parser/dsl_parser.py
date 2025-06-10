import os
from lark import Lark, UnexpectedInput

GRAMMAR_FILE = os.path.join(os.path.dirname(__file__), "dsl_grammar.lark")
with open(GRAMMAR_FILE, "r", encoding="utf-8") as f:
    GRAMMAR = f.read()
parser = Lark(GRAMMAR, parser="lalr", start="start")


def validate_dsl(dsl_code: str) -> bool:
    """
    Validate the given DSL code against the grammar.

    Args:
        dsl_code (str): The DSL code as a string.

    Returns:
        bool: True if valid, False if syntax error.
    """
    try:
        parser.parse(dsl_code)
        return True
    except UnexpectedInput:
        return False

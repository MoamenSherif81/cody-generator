import json
import os

from pydantic import BaseModel, Field

from Ai_Agents.models.models import ModelMessage
from LLM.Scheme.AnswerQuestion import AskQuestion


class AnswerQuestion(BaseModel):
    Response: str = Field(..., description="The Ai Agent Response of the request (don't contain code) just explanation")
_methinks: str = Field(..., description="DSL Code Corresponding to the situations")


dsl_grammar = """
// Entry point — enforces strict one-of-each block, ordered
start: maybe_header maybe_side_nav rows? maybe_footer

maybe_header: tag_header?
maybe_side_nav: tag_side_nav?
maybe_footer: tag_footer?

rows: tag_row (COMMA tag_row)*

tag_header: "header" attr_block?
tag_footer: "footer" attr_block?
tag_side_nav: "side_nav" attr_block?

tag_row: "row" attr_block? "{" row_body? "}"
row_body: (tag_box (COMMA tag_box)*)?

tag_box: "box" attr_block? "{" box_body? "}"
box_body: (leaf_tag (COMMA leaf_tag)*)?

leaf_tag: LEAF_TAG attr_block?

LEAF_TAG: "button" | "title" | "text" | "select_box" | "input" | "image"

// Attributes
attr_block: "<" attr_list? ">"
attr_list: attr (COMMA attr)*

attr: "args" "=" array_value       -> args_attribute
    | NAME "=" tuple_value         -> generic_attribute

// args=["a", "b"]
array_value: "[" string_list? "]"
string_list: ESCAPED_STRING (COMMA ESCAPED_STRING)*

// text=("hello"), color=(255,255,255)
tuple_value: "(" value_list? ")"
value_list: value (COMMA value)*

value: ESCAPED_STRING | NUMBER

COMMA: ","
COMMENT: /#[^\n]*/

%ignore COMMENT
%import common.CNAME -> NAME
%import common.ESCAPED_STRING
%import common.SIGNED_NUMBER -> NUMBER
%import common.WS
%ignore WS

"""


def AnswerPrompt(prom):
    """
    Builds strict system and user prompts for Gemini with DSL grammar and examples.
    Args:
        prom: The user prompt/question.
    Returns:
        Tuple of (instruction_message, user_message) as ModelMessage.
    """
    dsl_rules_path = os.path.abspath("Compiler_V3/Parser/dsl_grammar.lark")
    dsl_example_path = os.path.abspath("LLM/Backend/dsl_examples/code1.dsl")
    with open(dsl_example_path, 'r') as file:
        dsl_example = file.read()

    system_prompt = f"""
You are a DSL code generator for a strict frontend GUI language.
You MUST ONLY use tokens, nesting, and parameter syntax allowed by the provided Lark grammar.

# DSL Lark Grammar
{dsl_grammar}

# Container tokens (MUST use '{{}}'): [row, box]
# Leaf tokens (MUST NOT use '{{}}'): [button, input, select_box, title, text, image]

# Token Rules:
- Container tokens wrap their children with {{}}.
- Only place leaf tokens inside containers. Do NOT wrap leaf tokens in {{}}.
- Parameters must be sent in '<>' immediately after the token, in the format key=(\"value\").
  - Example: button<text=(\"OK\")>
- If a CSS attribute has a dash, replace it with an underscore (e.g., font-size → font_size).
- 'row' can ONLY contain 'box' tokens as direct children.
- 'box' can contain any element.
- Use only valid DSL tokens. DO NOT invent new tokens.
- Use only valid URLs and example images.
- Center elements visually whenever possible.
- String literals in the DSL must be enclosed in double quotes ("..."), as defined by ESCAPED_STRING in the grammar. Do not use single quotes.
- No introduction or explanation—output ONLY the DSL code and required JSON, nothing else.
- Make colors visually appealing but consistent.
- Don't add COMMA between row and  footer
- The grammar is STRICT. Invalid code will be REJECTED.
- Can't Add Parameter Value as list EXCEPT FOR header,side_nav,footer

# Good Example DSL:
{dsl_example}

# Bad Example DSL (WRONG):
box {"{}"}
button {"{}"}
# Correction: box {{ button<> }}

# Additional Bad DSL (Incorrect):
header <title=('Login Page')>
# Correction:
header <title=(\"Login Page\")>

# Additional Bad DSL (Incorrect):
select_box <options=([\"Excellent\", \"Good\", \"Fair\", \"Poor\", \"T\n])
# Correction:
select_box <text=("rating")>

# Additional Bad DSL (Incorrect):
header <title=\"Egypt Match Feedback\", args=[\"Home\"]>\n"
# Correction:
header <title=(\"Egypt Match Feedback\"), args=[\"Home\"]>\n"
# Response format:
{{
    "Dsl" : "The Dsl code you generated",
    "Response": "Your explanation of the code"
}}
# Repeat: Only output valid DSL code with string literals in double quotes and the
    **required JSON response{{
     "Dsl" : "The Dsl code you generated",
     "Response": "Your explanation of the code"
# }}**
"""

    user_message = ModelMessage(
        role="user",
        message=(
            f"## Pydantic Input Schema:\n"
            f"{json.dumps(AskQuestion.model_json_schema(), ensure_ascii=False)}\n\n"
            f"## Question:\n{prom}\n"
        )
    )

    instruction = ModelMessage(role="system", message=system_prompt)

    return instruction, user_message
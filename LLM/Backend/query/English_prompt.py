import json
import os

from Ai_Agents.models.models import ModelMessage
from LLM.Scheme.AnswerQuestion import AskQuestion

dsl_english_grammar = """
# DSL STRUCTURE RULES (FOLLOW EXACTLY)

## 1. OVERALL STRUCTURE
- A DSL file must contain these sections in this EXACT order:
  1. header (optional)
  2. side_nav (optional) 
  3. rows (one or more rows)
  4. footer (optional)

## 2. CONTAINER ELEMENTS (use curly braces {})
These elements MUST wrap their content in curly braces:
- `header` - appears at the top
- `side_nav` - appears on the side for navigation
- `footer` - appears at the bottom
- `row` - horizontal container that can ONLY contain `box` elements
- `box` - flexible container that can contain any leaf elements

## 3. LEAF ELEMENTS (NO curly braces)
These elements NEVER use curly braces:
- `button` - clickable button
- `title` - heading text
- `text` - regular text content
- `select_box` - dropdown selection
- `input` - text input field
- `image` - image display

## 4. ATTRIBUTE SYNTAX
- Attributes go in angle brackets < > immediately after the element name
- Format: element_name<attribute_name=("value")>
- ALWAYS use double quotes around string values: ("text here")
- NEVER use single quotes
- Multiple attributes separated by commas: element<attr1=("val1"), attr2=("val2")>
- For CSS properties with dashes, use underscores: font_size instead of font-size

## 5. NESTING RULES
- `row` can ONLY contain `box` elements as direct children
- `box` can contain any leaf elements (button, title, text, etc.)
- Use commas to separate multiple children at the same level
- Example: row { box { button, text }, box { title, input } }

## 6. SPECIAL ATTRIBUTES
- `args` attribute takes an array: args=["value1", "value2"]
- Only header, side_nav, and footer can have list-type parameters
- All other elements use single values in parentheses

## 7. SPACING AND COMMAS
- Use commas between elements at the same level
- NO comma between the last row and footer
- Proper spacing makes code readable

## 8. VALID EXAMPLE PATTERNS
Good:
- header<title=("Page Title")>
- row { box { button<text=("Click Me")> } }
- text<content=("Hello World"), color=("blue")>

Bad:
- header<title='Page Title'> (single quotes)
- button { } (leaf element with braces)
- box<options=["a", "b"]> (list in non-header element)
"""


def AnswerPrompt(prom):
    """
    Builds strict system and user prompts for Gemini with English DSL grammar and examples.
    Args:
        prom: The user prompt/question.
    Returns:
        Tuple of (instruction_message, user_message) as ModelMessage.
    """
    dsl_example_path = os.path.abspath("LLM/Backend/dsl_examples/code1.dsl")
    with open(dsl_example_path, 'r') as file:
        dsl_example = file.read()

    system_prompt = f"""
You are a DSL code generator for a strict frontend GUI language.
You MUST follow the English grammar rules provided below EXACTLY.

# DSL ENGLISH GRAMMAR RULES
{dsl_english_grammar}

# CRITICAL SYNTAX REQUIREMENTS:

## MUST add commas between TOKENS but not after HEADER,SIDE_NAVE,LAST ROW , FOOTER
## STRING VALUES:
- ALWAYS use double quotes: ("text here")
- NEVER use single quotes: ('text') ❌
- ALWAYS USE CIRCLE BRACKETS () ✅
- NEVER USE + , THERE IS NO CONCATENATION
- Example: button<text=("Submit")> ✅

## CONTAINER vs LEAF ELEMENTS:
- Containers (header, footer, side_nav, row, box) use curly braces {{}}
- Leaf elements (button, title, text, input, select_box, image) NEVER use curly braces
- Example: 
  - row {{ box {{ button<text=("OK")> }} }} ✅
  - button {{ }} ❌

## ATTRIBUTE FORMAT:
- Format: element<attribute=("value")>
- Multiple attributes: element<attr1=("val1"), attr2=("val2")>
- CSS properties: use underscores for dashes (font_size not font-size)

## NESTING HIERARCHY:
- row → can only contain → box
- box → can contain → any leaf elements
- Use commas between siblings: button, text, input

## ARRAY ATTRIBUTES (SPECIAL CASE):
- Only for header, side_nav, footer: args=["item1", "item2"]
- All other elements use single values: text=("content")

## STRUCTURAL ORDER:
1. header (optional)
2. side_nav (optional)
3. rows (required - one or more)
4. footer (optional)

# WORKING EXAMPLE:
{dsl_example}

# COMMON MISTAKES TO AVOID:
❌ button<text=('Click')> (single quotes)
❌ button {{ }} (leaf with braces)
❌ select_box<options=["a", "b"]> (list in non-header element)
❌ row {{ button }} (button directly in row, needs box)
❌ header <title=\"Page\", args=[\"Home\"]> (wrong quote format)
❌ text<content=("Total Points: 4,000")>

✅ button<text=("Click")> (double quotes in parentheses)
✅ row {{ box {{ button<text=("Click")> }} }} (proper nesting)
✅ header<title=("Page"), args=["Home"]> (correct format)
✅ text<text=("Total Points: 4,000")>

# OUTPUT FORMAT:
Return ONLY a JSON object with this exact structure:
{{
    "Dsl": "Your generated DSL code here",
    "Response": "Brief explanation of what the interface does"
}}

IMPORTANT REMINDERS:
- Use double quotes in parentheses for all string values: ("text")
- Container elements need curly braces, leaf elements don't
- Proper nesting: row → box → leaf elements
- Use commas between sibling elements
- Follow the structural order: header, side_nav, rows, footer
- Only output the JSON response, nothing else
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

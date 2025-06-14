import json
from textwrap import dedent
from LLM.Backend.query.prompt import AnswerQuestion

GRAMMAR = dedent("""
    start: maybe_header comma? maybe_side_nav comma? maybe_body comma? maybe_footer
    maybe_header: tag_header?
    maybe_side_nav: tag_side_nav?
    maybe_body: tag_body?
    maybe_footer: tag_footer?
    comma: COMMA
    tag_header: "header" attr_block?
    tag_footer: "footer" attr_block?
    tag_side_nav: "side_nav" attr_block?
    tag_body: "body" attr_block? "{" rows? "}"
    rows: tag_row (COMMA tag_row)*
    tag_row: "row" attr_block? "{" tag_boxes? "}"
    tag_boxes: tag_box (COMMA tag_box)*
    tag_box: "box" attr_block? "{" leaf_tags? "}"
    leaf_tags: leaf_tag (COMMA leaf_tag)*
    leaf_tag: LEAF_TAG attr_block?
    LEAF_TAG: "button" | "title" | "text" | "select_box" | "input" | "image"

    // Attributes
    attr_block: "<" attr_list? ">"
    attr_list: attr (COMMA attr)* COMMA?
    attr: NAME "=" attr_value
    attr_value: ESCAPED_STRING | array_value
    array_value: "[" string_list? "]"
    string_list: ESCAPED_STRING (COMMA ESCAPED_STRING)* COMMA?
    COMMA: ","
    COMMENT: /#[^\\n]*/
    %ignore COMMENT
    %import common.CNAME -> NAME
    %import common.ESCAPED_STRING
    %import common.WS
    %ignore WS
""")

INSTRUCTIONS = dedent(f"""
    # You are a professional Frontend Developer that can generate webpages using our own custom DSL.
    # Generate the DSL for the provided situation.
    # Use only DSL Tokens.
    # You can pass any number of CSS attributes to any token by sending key-value pairs inside <>.
    ## Example: title<background_color="#23433", align_items="center">
    ## For CSS attributes containing '-', use '_' instead.
    # You can send text to any token by send parameter text
    ## title<text="hello">
    ## image<src="www.google.com">
    # You can pass args to header,footer,side_nav
    ## example header<args=["title1","title2","title3"]>
    # Should add COMMA between each token and another
    # Do not include any introduction or conclusion.
    # Use a visually appealing, simple color scheme with all colors in #xxxxx format.
    # Be creative.
    # Make elements at center as possible
    # MAKE THE PAGE LOOK MODERN
    # SHOULD FOLLOW THE LARK GRAMMAR RULES
    # MAKE IT COLORFUL AND HAVE THEME
""")

def answer_prompt_with_open_ai(prompt: str) -> str:
    return dedent(f"""\
        role: system
        grammar.lark
        ```
        {GRAMMAR}
        ```

        {INSTRUCTIONS}

        role: user
        prompt: {prompt}
    """)

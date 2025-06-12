from typing import Dict, Any

from lark import Tree

from Compiler_V3 import validate_dsl, generate_ast
from Compiler_V3.Parser.transformer import ASTNode


def format_attributes(attributes: Dict[str, Any]) -> str:
    """Format the attributes of an AST node into a string."""
    if not attributes:
        return ""
    formatted_attrs = []
    for key, value in attributes.items():
        if key == "args":
            if isinstance(value, str):
                formatted_value = "[" + f'"{value}"' + "]"
            elif isinstance(value, list):
                value = [v for v in value if v != ',']
                formatted_value = "[" + ", ".join(f'"{v}"' for v in value) + "]"
            else:
                formatted_value = "[]"
            formatted_attrs.append(f"args={formatted_value}")
        else:
            formatted_value = "(" + ", ".join(f'"{v}"' if isinstance(v, str) else str(v) for v in value) + ")"
            formatted_attrs.append(f"{key}={formatted_value}")
    return " <" + ", ".join(formatted_attrs) + ">"


def format_node(node: ASTNode, indent_level: int, spc: str) -> str:
    """Recursively format an AST node with proper indentation."""
    if node is None:
        return ""
    indent = spc * indent_level
    tag = node.tag
    attr_block = format_attributes(node.attributes)

    if node.children:
        formatted_children = []
        for i, child in enumerate(node.children):
            formatted_child = format_node(child, indent_level + 1, spc)
            if formatted_child and i < len(node.children) - 1:
                formatted_child += ","
            formatted_children.append(formatted_child)
        children_str = "\n".join(fc for fc in formatted_children if fc)
        return f"{indent}{tag}{attr_block} {{\n{children_str}\n{indent}}}" if children_str else f"{indent}{tag}{attr_block}"
    else:
        # check if the tag is container
        if tag in ["row","box"]:
            return f"{indent}{tag}" + "{}"
        return f"{indent}{tag}{attr_block}"


def linter_formatter(dsl_code: str, spc: str = "    ") -> str:
    """
    Format DSL code into a well-structured string.

    Args:
        dsl_code (str): The input DSL code to format.
        spc (str): The spacing unit for indentation (default is four spaces).

    Returns:
        str: The formatted DSL code or an error message if invalid.
    """
    # Step 1: Validate the DSL code
    if dsl_code.strip() == "":
        return ""
    is_valid, error = validate_dsl(dsl_code)
    if not is_valid:
        return f"Error: {error}"

    # Step 2: Generate the AST
    ast = generate_ast(dsl_code)
    # Step 3: Format the AST
    formatted_parts = []
    for item in ast:
        if isinstance(item, Tree):
            item = item.children
        if isinstance(item, list):  # Handle the rows list
            formatted_rows = [format_node(row, 0, spc) for row in item if row]
            formatted_rows = [fr for fr in formatted_rows if fr]
            if formatted_rows:
                formatted_parts.append(",\n".join(formatted_rows))
        elif item:  # Handle single nodes like header, side_nav, footer
            formatted_part = format_node(item, 0, spc)
            if formatted_part:
                formatted_parts.append(formatted_part)

    return "\n".join(formatted_parts) if formatted_parts else ""

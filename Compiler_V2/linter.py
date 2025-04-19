import sys
from typing import Dict

from .models import ASTNode
from .parser import tokenize, parse

tabSize = " "


def lint_and_format_dsl(dsl: str, tag_mappings: Dict[str, Dict], opening_tag: str, closing_tag: str) -> str:
    """Lint and reformat DSL code using the AST."""
    try:
        tokens = tokenize(dsl, opening_tag, closing_tag)

        if not tokens:
            raise ValueError("Empty DSL input")

        # Validate tokens
        valid_leaf_tags = {tag for tag in tag_mappings if tag in ["input", "select-box", "title", "text", "button"]}
        for i, token in enumerate(tokens):
            if token not in tag_mappings and token not in [opening_tag, closing_tag, ',', '<', '>'] and not (
                    token.startswith('<') and token.endswith('>')):
                raise ValueError(f"Invalid DSL: Unknown token '{token}'")
            if i < len(tokens) - 1 and token == ',' and tokens[i + 1] == ',':
                raise ValueError("Invalid DSL: Consecutive commas detected")

        ast = parse(tokens, tag_mappings, opening_tag, closing_tag)

        def validate_node(node: ASTNode, parent_tag: str = None):
            if node.tag not in tag_mappings and node.tag != 'root':
                raise ValueError(f"Invalid DSL: Invalid tag '{node.tag}'")
            # if not node.children and node.tag != 'root' and node.tag not in valid_leaf_tags:
            #     raise ValueError(f"Invalid DSL: Empty block for tag '{node.tag}'")
            for child in node.children:
                validate_node(child, node.tag)

        validate_node(ast)

        def format_node(node: ASTNode, indent: int = 0) -> str:
            if node.tag == 'root':
                return ",\n".join(format_node(child, indent) for child in node.children)

            result = []
            tag_line = node.tag
            if node.attributes:
                attr_parts = []
                for attr_name, attr_value in node.attributes.items():
                    if attr_name == "color" and isinstance(attr_value, tuple):
                        attr_parts.append(f"color=({attr_value[0]},{attr_value[1]},{attr_value[2]})")
                    else:
                        attr_parts.append(f"{attr_name}={attr_value}")
                tag_line += f" <{','.join(attr_parts)}>"
            tag_line += f" {opening_tag}" if node.children else ""
            result.append(f"{tabSize}" * indent + tag_line)

            if node.children:
                for i, child in enumerate(node.children):
                    child_formatted = format_node(child, indent + 1)
                    for line in child_formatted.splitlines():
                        result.append(f"{tabSize}" * (indent + 1) + line.rstrip())
                    if i < len(node.children) - 1:
                        result[-1] += ","
                result.append(f"{tabSize}" * indent + closing_tag)

            return "\n".join(result)

        formatted_dsl = format_node(ast)
        return formatted_dsl + "\n" if formatted_dsl else ""

    except ValueError as e:
        print(f"DSL Linting Error: {str(e)}", file=sys.stderr)
        raise
    except Exception as e:
        print(f"DSL Linting Error: Failed to lint DSL: {str(e)}", file=sys.stderr)
        raise ValueError(f"Failed to lint DSL: {str(e)}")

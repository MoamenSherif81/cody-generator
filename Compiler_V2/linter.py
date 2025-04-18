from typing import Dict
from .parser import tokenize, parse
from .models import ASTNode
import sys
tab=" "

def lint_and_format_dsl(dsl: str, tag_mappings: Dict[str, str], opening_tag: str, closing_tag: str) -> str:
    """Lint and reformat DSL code using the AST."""
    try:
        # Tokenize DSL
        tokens = tokenize(dsl, opening_tag, closing_tag)

        # Basic token validation
        if not tokens:
            raise ValueError("Empty DSL input")

        # Check for consecutive commas or invalid tokens
        for i in range(len(tokens) - 1):
            if tokens[i] == ',' and tokens[i + 1] == ',':
                raise ValueError("Invalid DSL: Consecutive commas detected")
            if tokens[i] not in tag_mappings and tokens[i] not in [opening_tag, closing_tag, ',']:
                raise ValueError(f"Invalid DSL: Unknown token '{tokens[i]}'")

        # Parse into AST
        ast = parse(tokens, tag_mappings, opening_tag, closing_tag)

        # Validate AST
        def validate_node(node: ASTNode, parent_tag: str = None):
            if node.tag not in tag_mappings:
                raise ValueError(f"Invalid DSL: Invalid tag '{node.tag}'")
            if not node.children and node.tag != 'root' and tag_mappings[node.tag] == '[]':
                raise ValueError(f"Invalid DSL: Empty block for tag '{node.tag}'")
            for child in node.children:
                validate_node(child, node.tag)

        validate_node(ast)

        # Reformat DSL from AST
        def format_node(node: ASTNode, indent: int = 0) -> str:
            if node.tag == 'root':
                # Root node: format children as top-level tags
                return ",\n".join(format_node(child, indent) for child in node.children)

            # Format tag and its children
            result = []
            result.append(f"{tab}" * indent + node.tag + " {")
            if node.children:
                for i, child in enumerate(node.children):
                    child_formatted = format_node(child, indent + 1)
                    for line in child_formatted.splitlines():
                        result.append(f"{tab}" * (indent + 1) + line.rstrip())
                    if i < len(node.children) - 1:
                        result[-1] += ","
            result.append(f"{tab}" * indent + closing_tag)
            return "\n".join(result)

        formatted_dsl = format_node(ast)
        return formatted_dsl + "\n" if formatted_dsl else ""

    except ValueError as e:
        print(f"DSL Linting Error: {str(e)}", file=sys.stderr)
        raise
    except Exception as e:
        print(f"DSL Linting Error: Failed to lint DSL: {str(e)}", file=sys.stderr)
        raise ValueError(f"Failed to lint DSL: {str(e)}")
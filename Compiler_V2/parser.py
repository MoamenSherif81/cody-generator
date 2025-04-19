import re
from typing import List, Dict, Tuple

from .models import ASTNode


def tokenize(dsl: str, opening_tag: str, closing_tag: str) -> List[str]:
    """Tokenize DSL string into tags, braces, commas, and attribute specifications."""
    opening_tag_escaped = re.escape(opening_tag)
    closing_tag_escaped = re.escape(closing_tag)
    attr_open = re.escape("<")
    attr_close = re.escape(">")

    # Match tags, braces, commas, and attribute blocks
    pattern = rf'({opening_tag_escaped}|{closing_tag_escaped}|,|[a-zA-Z][a-zA-Z0-9\-]*|{attr_open}\s*[^>]*?\s*{attr_close})'

    tokens = re.findall(pattern, dsl.strip())
    return tokens


def parse(tokens: List[str], tag_mappings: Dict[str, Dict], opening_tag: str, closing_tag: str) -> ASTNode:
    """Parse tokens into an AST, handling select-box and attributes."""

    def is_attribute_token(token: str) -> bool:
        """Check if token is an attribute specification."""
        return bool(re.match(r'<\s*[^>]*?\s*>', token))

    def parse_attributes(token: str) -> Dict[str, any]:
        """Extract and validate attributes from token."""
        attributes = {}
        content = re.match(r'<\s*([^>]*?)\s*>', token)
        if not content:
            raise ValueError(f"Invalid attribute format: {token}")
        attr_string = content.group(1)

        attr_pairs = []
        current = ""
        paren_count = 0
        for char in attr_string + ",":
            if char == "(":
                paren_count += 1
            elif char == ")":
                paren_count -= 1
            elif char == "," and paren_count == 0:
                if current.strip():
                    attr_pairs.append(current.strip())
                current = ""
                continue
            current += char

        for pair in attr_pairs:
            if "=" not in pair:
                raise ValueError(f"Invalid attribute pair: {pair}")
            key, value = map(str.strip, pair.split("=", 1))

            if key == "color":
                match = re.match(r'\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', value)
                if not match:
                    raise ValueError(f"Invalid color format: {value}")
                r, g, b = map(int, match.groups())
                if not all(0 <= x <= 255 for x in [r, g, b]):
                    raise ValueError(f"Invalid color value: RGB values must be between 0 and 255 in {value}")
                attributes[key] = (r, g, b)
            else:
                attributes[key] = value

        return attributes

    def parse_tokens(index: int, current_tag: str = None) -> Tuple[ASTNode, int]:
        if index >= len(tokens):
            raise ValueError("Unexpected end of input")

        token = tokens[index]
        if token == closing_tag:
            return None, index

        if token in tag_mappings:
            node = ASTNode(tag=token)
            index += 1

            # Check for attribute specification
            attributes = {}
            if index < len(tokens) and is_attribute_token(tokens[index]):
                attributes = parse_attributes(tokens[index])
                index += 1

            # Parse children if opening tag follows
            if index < len(tokens) and tokens[index] == opening_tag:
                index += 1
                while index < len(tokens) and tokens[index] != closing_tag:
                    if tokens[index] == ',':
                        index += 1
                        continue
                    child, index = parse_tokens(index)
                    if child:
                        node.children.append(child)
                if index >= len(tokens) or tokens[index] != closing_tag:
                    raise ValueError(f"Missing closing tag for {token}")
                index += 1

            node.attributes = attributes
            return node, index

        raise ValueError(f"Invalid token: {token}")

    # Create root node
    root = ASTNode(tag="root")
    index = 0
    while index < len(tokens):
        if tokens[index] == ',':
            index += 1
            continue
        node, index = parse_tokens(index)
        if node:
            root.children.append(node)

    return root

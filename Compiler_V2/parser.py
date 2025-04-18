from typing import List, Tuple
from .models import ASTNode


def tokenize(dsl: str, opening_tag: str, closing_tag: str) -> List[str]:
    """Tokenize DSL input into tags, commas, and braces, allowing hyphens in tags."""
    tokens = []
    i = 0
    while i < len(dsl):
        char = dsl[i]
        if char.isspace():
            i += 1
            continue
        if char in [opening_tag, closing_tag, ',']:
            tokens.append(char)
            i += 1
        else:
            # Collect tag name
            start = i
            # Ensure tag starts with a letter
            if i < len(dsl) and not dsl[i].isalpha():
                raise ValueError(f"Tag must start with a letter at position {i}: {dsl[i:]}")
            while i < len(dsl) and (dsl[i].isalnum() or dsl[i] == '-') and dsl[i] not in [opening_tag, closing_tag, ',',
                                                                                          ' ']:
                i += 1
            tag = dsl[start:i].strip()
            if tag:
                tokens.append(tag)
    return tokens


def parse(tokens: List[str], tag_mappings: dict, opening_tag: str, closing_tag: str) -> ASTNode:
    """Parse tokens into an AST with a root node containing all top-level tags."""
    if not tokens:
        raise ValueError("Empty DSL input")

    def parse_recursive(index: int) -> Tuple[ASTNode, int]:
        """Parse tokens starting at index, return node and next index."""
        if index >= len(tokens) or tokens[index] in [opening_tag, closing_tag, ',']:
            raise ValueError(
                f"Expected tag at position {index}, found: {tokens[index] if index < len(tokens) else 'EOF'}")

        if tokens[index] not in tag_mappings or tokens[index] in ["opening-tag", "closing-tag"]:
            raise ValueError(f"Invalid tag: {tokens[index]}")

        node = ASTNode(tag=tokens[index], children=[])
        index += 1

        # Check for opening brace
        if index < len(tokens) and tokens[index] == opening_tag:
            index += 1
            while index < len(tokens) and tokens[index] != closing_tag:
                child_node, new_index = parse_recursive(index)
                node.children.append(child_node)
                index = new_index
                # Expect comma or closing brace
                if index < len(tokens) and tokens[index] == ',':
                    index += 1
                elif index < len(tokens) and tokens[index] != closing_tag:
                    raise ValueError("Expected ',' or '}'")
            if index >= len(tokens) or tokens[index] != closing_tag:
                raise ValueError("Unmatched opening brace")
            index += 1
        return node, index

    root_node = ASTNode(tag="root", children=[])
    index = 0
    while index < len(tokens):
        node, new_index = parse_recursive(index)
        root_node.children.append(node)
        index = new_index
        # Expect comma or end of input
        if index < len(tokens) and tokens[index] == ',':
            index += 1
        elif index < len(tokens):
            raise ValueError(f"Expected ',' or end of input at position {index}, found: {tokens[index]}")

    return root_node
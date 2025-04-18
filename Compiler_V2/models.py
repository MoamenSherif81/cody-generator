from typing import List

class ASTNode:
    """Represents a node in the DSL AST."""
    def __init__(self, tag: str, children: List['ASTNode'] = None):
        self.tag = tag
        self.children = children or []
from typing import List, Dict, Any


class ASTNode:
    def __init__(self, tag: str, children: List['ASTNode'] = None, attributes: Dict[str, Any] = None):
        self.tag = tag  # Stores the tag name (e.g., 'row', 'box')
        self.children = children if children is not None else []
        self.attributes = attributes if attributes is not None else {}

from dataclasses import dataclass
from typing import List, Dict, Any, Tuple


class ASTNode:
    def __init__(self, tag: str, children: List['ASTNode'] = None, attributes: Dict[str, Any] = None):
        self.tag = tag  # Stores the tag name (e.g., 'row', 'box')
        self.children = children if children is not None else []
        self.attributes = attributes if attributes is not None else {}

    def __repr__(self):
        return f"ASTNode(tag={self.tag}, attributes={self.attributes}, children={len(self.children)})"


@dataclass
class TagConfig:
    htmlTag: str
    cssClasses: List[str]
    cssAttributes: Dict[str, str]
    textLimit: int
    defaultColor: Tuple[int, int, int]

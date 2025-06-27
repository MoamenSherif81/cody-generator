from lark import Transformer, Token, Tree
from Compiler_V3.models import ASTNode


class DSLTransformer(Transformer):
    def start(self, items):
        # Return a list of valid ASTNode (body, header, etc.)
        return [item for item in items if isinstance(item, ASTNode)]

    def maybe_header(self, items):
        return items[0] if items else None

    def maybe_side_nav(self, items):
        return items[0] if items else None

    def maybe_body(self, items):
        return items[0] if items else None

    def maybe_footer(self, items):
        return items[0] if items else None

    def tag_header(self, items):
        attrs = items[0] if items else {}
        return ASTNode("header", attributes=attrs)

    def tag_footer(self, items):
        attrs = items[0] if items else {}
        return ASTNode("footer", attributes=attrs)

    def tag_side_nav(self, items):
        attrs = items[0] if items else {}
        return ASTNode("side_nav", attributes=attrs)

    def tag_body(self, items):
        attrs = {}
        children = []
        for item in items:
            if isinstance(item, dict):
                attrs = item
            elif isinstance(item, list):
                children = item  # list of rows
        return ASTNode("body", attributes=attrs, children=children)

    def rows(self, items):
        return items  # list of ASTNode(row)

    def tag_row(self, items):
        attrs = {}
        children = []
        for item in items:
            if isinstance(item, dict):
                attrs = item
            elif isinstance(item, list):
                children = item  # list of boxes
        return ASTNode("row", attributes=attrs, children=children)

    def tag_boxes(self, items):
        return items  # list of ASTNode(box)

    def tag_box(self, items):
        attrs = {}
        children = []
        for item in items:
            if isinstance(item, dict):
                attrs = item
            elif isinstance(item, list):
                children = item  # list of leaf_tags
        return ASTNode("box", attributes=attrs, children=children)

    def leaf_tags(self, items):
        return items  # list of ASTNode leaf tags

    def leaf_tag(self, items):
        tag_name = items[0].value  # e.g. title, text
        attrs = items[1] if len(items) > 1 else {}
        return ASTNode(tag_name, attributes=attrs)

    def attr_block(self, items):
        if not items:
            return {}
        # Flatten if attr_list is inside
        if len(items) == 1 and isinstance(items[0], list):
            items = items[0]
        attrs = {}
        for item in items:
            if isinstance(item, Tree) and item.data == "attr":
                key_token = item.children[0]
                value = item.children[1]
                if isinstance(value, Tree) and value.data == "attr_value":
                    value = value.children[0]
                key = key_token.value
                attrs[key] = value
        return attrs

    def attr_list(self, items):
        return items

    def attr(self, items):
        return Tree("attr", items)

    def attr_value(self, items):
        return items[0]

    def array_value(self, items):
        return items[0] if items else []

    def string_list(self, items):
        return [item for item in items if isinstance(item, str)]

    def ESCAPED_STRING(self, token):
        return token.value.strip('"')

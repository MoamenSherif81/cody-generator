from lark import Transformer, Token

from Compiler_V3.models import ASTNode


class DSLTransformer(Transformer):
    def start(self, items):
        return [item for item in items if item is not None]

    def maybe_header(self, items):
        return items[0] if items else None

    def maybe_side_nav(self, items):
        return items[0] if items else None

    def maybe_footer(self, items):
        return items[0] if items else None

    def tag_header(self, items):
        attrs = items[0] if items else {}
        return ASTNode("header", children=[], attributes=attrs)

    def tag_footer(self, items):
        attrs = items[0] if items else {}
        return ASTNode("footer", children=[], attributes=attrs)

    def tag_side_nav(self, items):
        attrs = items[0] if items else {}
        return ASTNode("side_nav", children=[], attributes=attrs)

    def tag_row(self, items):
        attrs = {}
        children = []
        for item in items:
            if isinstance(item, dict):
                attrs = item
            elif isinstance(item, list):
                children = item
        return ASTNode("row", children=children, attributes=attrs)

    def row_body(self, items):
        # Filter out Token objects, keeping only ASTNode objects
        return [item for item in items if not isinstance(item, Token)]

    def tag_box(self, items):
        attrs = {}
        children = []
        for item in items:
            if isinstance(item, dict):
                attrs = item
            elif isinstance(item, list):
                children = item
        return ASTNode("box", children=children, attributes=attrs)

    def box_body(self, items):
        # Filter out Token objects, keeping only ASTNode objects
        return [item for item in items if not isinstance(item, Token)]

    def leaf_tag(self, items):
        tag_name = items[0].value  # tag name like 'title', 'button', etc.
        attrs = items[1] if len(items) > 1 else {}
        return ASTNode(tag_name, children=[], attributes=attrs)

    def attr_block(self, items):
        """Safely handle attribute blocks that might have missing values"""
        if not items:
            return {}

        attributes = {}

        # Handle case where items is a single list containing all attributes
        if len(items) == 1 and isinstance(items[0], list):
            items = items[0]

        # Filter out comma tokens and process only tuples
        for item in items:
            # Skip comma tokens
            if isinstance(item, Token) and item.type == 'COMMA':
                continue

            if isinstance(item, tuple) and len(item) == 2:
                key, value = item

                # If value is a nested list, flatten it
                if isinstance(value, list) and len(value) == 1:
                    value = value[0]

                # Now we have the final key-value pair
                attributes[key] = value
            else:
                # Only raise error for non-comma tokens that aren't proper tuples
                if not (isinstance(item, Token) and item.type == 'COMMA'):
                    raise ValueError(f"Invalid attribute format: {item}")

        return attributes

    def attr_list(self, items):
        return items

    def args_attribute(self, items):
        return ("args", items[0])  # items[0] is already the transformed array_value

    def generic_attribute(self, items):
        """Safely handle attributes and ensure the correct number of items"""
        if len(items) == 1:
            return (items[0], None)  # If there's no value, assign None
        elif len(items) == 2:
            return (items[0].value, items[1])  # (key, value) pair
        else:
            raise ValueError(f"Unexpected attribute format: {items}")

    def array_value(self, items):
        return items[0] if items else []  # items[0] is string_list or None

    def string_list(self, items):
        return [item for item in items if isinstance(item, str)]

    def tuple_value(self, items):
        # Filter out comma tokens from tuple values too
        filtered_items = [item for item in items if not (isinstance(item, Token) and item.type == 'COMMA')]
        return filtered_items

    def value_list(self, items):
        # Filter out comma tokens from value lists
        filtered_items = [item for item in items if not (isinstance(item, Token) and item.type == 'COMMA')]
        return filtered_items

    def value(self, items):
        return items[0]

    def ESCAPED_STRING(self, token):
        return token.value.strip('"')

    def NUMBER(self, token):
        return float(token)

    def rows(self, items):
        # If there's a specific rule for multiple rows
        return [item for item in items if not isinstance(item, Token)]

    # Other methods for header, side_nav, row, box, etc.
    def row(self, items):
        return ASTNode(tag="row", children=items)

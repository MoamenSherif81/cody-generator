from lark import Transformer, Token


class DSLTransformer(Transformer):
    """Transforms the parse tree into a structured AST."""

    def start(self, items):
        return items  # List of rows

    def row(self, items):
        attrs = items[0] if items and isinstance(items[0], dict) and "attributes" in items[0] else {}
        content = items[1] if len(items) > 1 else []
        return {"type": "row", "attributes": attrs, "content": content}

    def box(self, items):
        attrs = items[0] if items and isinstance(items[0], dict) and "attributes" in items[0] else {}
        content = items[1] if len(items) > 1 else []
        return {"type": "box", "attributes": attrs, "content": content}

    def content(self, items):
        return items  # List of elements

    def element(self, items):
        return items[0]  # Either container or leaf

    def container(self, items):
        return items[0]  # Either row or box

    def leaf(self, items):
        return items[0]  # Either button, title, text, select_box, or input

    def button(self, items):
        attrs = items[0] if items and isinstance(items[0], dict) and "attributes" in items[0] else {}
        text = items[1] if len(items) > 1 else None
        return {"type": "button", "attributes": attrs, "text": text}

    def title(self, items):
        attrs = items[0] if items and isinstance(items[0], dict) and "attributes" in items[0] else {}
        text = items[1] if len(items) > 1 else None
        return {"type": "title", "attributes": attrs, "text": text}

    def text(self, items):
        attrs = items[0] if items and isinstance(items[0], dict) and "attributes" in items[0] else {}
        text = items[1] if len(items) > 1 else None
        return {"type": "text", "attributes": attrs, "text": text}

    def select_box(self, items):
        attrs = items[0] if items and isinstance(items[0], dict) and "attributes" in items[0] else {}
        text = items[1] if len(items) > 1 else None
        return {"type": "select-box", "attributes": attrs, "text": text}

    def input(self, items):
        attrs = items[0] if items and isinstance(items[0], dict) and "attributes" in items[0] else {}
        text = items[1] if len(items) > 1 else None
        return {"type": "input", "attributes": attrs, "text": text}

    def attributes(self, items):
        return {"attributes": dict(items)}

    def attribute(self, items):
        return (items[0], items[1])  # (attr_name, attr_value)

    def attr_name(self, items):
        # Handle both single token and list of items
        if isinstance(items, list):
            token = items[0]
        else:
            token = items

        if isinstance(token, Token):
            return token.value
        else:
            return str(token)

    def attr_value(self, items):
        return items[0]  # rgb_color, text_value, or size_value

    def rgb_color(self, items):
        return {"type": "color", "value": tuple(map(int, items))}

    def text_value(self, items):
        return {"type": "text", "value": items[0]}

    def size_value(self, items):
        return {"type": "size", "value": int(items[0]), "unit": "px"}

    def NUMBER(self, items):
        # Handle both single token and list of items
        if isinstance(items, list):
            token = items[0]
        else:
            token = items

        if isinstance(token, Token):
            return int(token.value)
        else:
            return int(str(token))

    def ESCAPED_STRING(self, items):
        # Handle both single token and list of items
        if isinstance(items, list):
            token = items[0]
        else:
            token = items

        if isinstance(token, Token):
            return token.value.strip('"')
        else:
            return str(token).strip('"')
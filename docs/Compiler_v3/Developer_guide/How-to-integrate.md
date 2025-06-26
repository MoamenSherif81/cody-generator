# How to Integrate

This guide explains how to integrate with the DSL compiler by using the **AST (Abstract Syntax Tree)** as the main integration point. Once you generate the AST, you can implement your own custom mapper to transform it into any target format such as HTML, React, Flutter, or desktop GUI libraries.

---

## Integration Strategy

The compiler is designed to be pluggable. Once the DSL code is validated and parsed, it becomes a structured tree of Python objects. You can traverse this tree and map each node (`ASTNode`) into your preferred output language or UI component.

---

## Example: Generate the AST and Compile

Here is a basic example using the compiler APIs:

```python
from Compiler_V3 import validate_and_generate_ast, compile_to_web

# Your DSL code string
dsl_code = """
body {
  row {
    box {
      title <text="Hello">,
      text <content="Welcome to Cody">
    }
  }
}
"""

# Step 1: Validate and generate AST
ok, ast, error = validate_and_generate_ast(dsl_code)
if not ok:
    print("Error:", error)
else:
    print("AST Tree:", ast)

# Step 2 (optional): Compile to HTML/CSS
html, css, error = compile_to_web(dsl_code)
```

---

## AST Structure

The AST is made of `ASTNode` objects. Each tag in the DSL becomes an `ASTNode` with a `tag` name, optional `attributes`, and a list of child nodes.

### ASTNode Class

```python
class ASTNode:
    def __init__(self, tag: str, children: List['ASTNode'] = None, attributes: Dict[str, Any] = None):
        self.tag = tag  # Stores the tag name (e.g., 'row', 'box')
        self.children = children if children is not None else []
        self.attributes = attributes if attributes is not None else {}

    def __repr__(self):
        return f"ASTNode(tag={self.tag}, attributes={self.attributes}, children={len(self.children)})"
```

---

## Example Output from AST

For the sample DSL code above, the AST may look like this:

```python
[
  ASTNode(
    tag='body',
    children=[
      ASTNode(
        tag='row',
        children=[
          ASTNode(
            tag='box',
            children=[
              ASTNode(tag='title', attributes={'text': 'Hello'}, children=[]),
              ASTNode(tag='text', attributes={'content': 'Welcome to Cody'}, children=[])
            ]
          )
        ]
      )
    ]
  )
]
```

---

You can now write your own recursive function to traverse this AST and convert it to any UI format you want.

Let us know if you need a template for a specific platform.

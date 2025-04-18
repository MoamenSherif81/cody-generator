import re
from typing import Set, Dict

from bs4 import BeautifulSoup

from .models import ASTNode
import random
import string
import cssutils

# HTML template to wrap the generated content
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DSL Example</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
{content}
</body>
</html>"""


def generate_html_template(content: str) -> str:
    """Wrap HTML content in the template."""
    soup = BeautifulSoup(HTML_TEMPLATE.format(content=content), "html.parser").prettify()
    return soup


def generate_html(node: ASTNode, tag_mappings: Dict[str, str], text_limits: Dict[str, int], used_classes: Set[str],
                  indent: int = 0) -> str:
    """Generate HTML from AST node with proper indentation and random text."""
    template = tag_mappings.get(node.tag)
    if not template:
        raise ValueError(f"Unknown tag: {node.tag}")

    # Extract CSS classes from the template
    classes = re.findall(r"class='([^']*)'", template)
    for class_list in classes:
        used_classes.update(class_list.split())

    # Generate random text based on text_limit
    max_limit = text_limits.get(node.tag, 0)
    text_limit = random.randint(1, max_limit) if max_limit > 0 else 0
    random_text = ""
    if text_limit > 0:
        random_text = "".join(random.choice(string.ascii_lowercase) for _ in range(text_limit))

    # Generate children HTML
    children_html = ""
    for child in node.children:
        children_html += generate_html(child, tag_mappings, text_limits, used_classes, indent + 2)

    # Replace [] with random text and/or children HTML
    content = random_text + children_html
    if content:
        html = template.replace("[]", "\n" + content + " " * indent)
    else:
        html = template.replace("[]", "")

    # Add indentation
    lines = html.split("\n")
    indented_lines = [" " * indent + line if line.strip() else line for line in lines]
    return "\n".join(indented_lines)


def filter_css(css_file: str, used_classes: Set[str]) -> str:
    """Filter CSS to include only styles for used classes."""
    try:
        with open(css_file, 'r') as f:
            css_content = f.read()
    except FileNotFoundError:
        raise ValueError(f"CSS file {css_file} not found")

    # Split CSS into blocks (simple parsing)
    blocks = []
    current_block = []
    in_block = False
    for line in css_content.split("\n"):
        line = line.strip()
        if not line:
            continue
        if line.endswith("{") and not in_block:
            in_block = True
            current_block.append(line)
        elif line == "}" and in_block:
            current_block.append(line)
            blocks.append("\n".join(current_block))
            current_block = []
            in_block = False
        elif in_block:
            current_block.append(line)
        else:
            blocks.append(line)

    # Filter blocks for used classes
    filtered_blocks = []
    for block in blocks:
        # Extract selector (before first '{')
        selector = block.split("{")[0].strip()
        # Handle multiple selectors (e.g., "select, input")
        selectors = [s.strip() for s in selector.split(",")]
        # Check if any selector is a used class (with or without leading .)
        if any(
                s == f".{c}" or s == c or c in s.split() for c in used_classes for s in selectors
        ):
            filtered_blocks.append(block)

    return "\n\n".join(filtered_blocks)
def generate_css_template(content: str) -> str:
    CSS = """*{
      margin: 0;
    }

    body{
      padding: 24px;
      box-sizing: border-box;
      background-color: white;
      font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
    }\n
    """
    CSS += content
    return CSS

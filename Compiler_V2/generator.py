import random
import string
from typing import Dict, Set, List

from .models import ASTNode


def generate_random_text(length: int) -> str:
    """Generate random text of specified length."""
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def generate_html(node: ASTNode, tag_mappings: Dict[str, Dict], used_classes: Set[str], dynamic_css_rules: List[str],
                  indent: int = 0) -> str:
    """Generate HTML string from AST with proper indentation and dynamic CSS classes."""
    if node.tag == "root":
        return "\n".join(
            generate_html(child, tag_mappings, used_classes, dynamic_css_rules, indent) for child in node.children)

    # Get tag configuration
    tag_config = tag_mappings.get(node.tag, {})
    html_tag = tag_config.get("htmlTag", "")
    css_classes = tag_config.get("cssClasses", [])
    css_attributes = tag_config.get("cssAttributes", {})
    text_limit = tag_config.get("textLimit", 0)

    # Add base classes to used_classes
    for cls in css_classes:
        used_classes.add(cls)

    # Generate dynamic CSS classes for configured attributes
    additional_classes = []
    for attr_name, attr_value in node.attributes.items():
        if attr_name in css_attributes:
            css_property = css_attributes[attr_name]
            if attr_name == "color" and isinstance(attr_value, tuple):
                class_name = f"{attr_name}-{attr_value[0]}-{attr_value[1]}-{attr_value[2]}"
                css_rule = f".{class_name} {{ {css_property}: rgb({attr_value[0]},{attr_value[1]},{attr_value[2]}); }}"
            else:
                class_name = f"{attr_name}-{attr_value.replace(' ', '-')}"
                css_rule = f".{class_name} {{ {css_property}: {attr_value}; }}"
            additional_classes.append(class_name)
            used_classes.add(class_name)
            if css_rule not in dynamic_css_rules:
                dynamic_css_rules.append(css_rule)

    # Combine all classes
    all_classes = css_classes + additional_classes
    class_attr = f" class='{' '.join(all_classes)}'" if all_classes else ""

    # Format style attribute for non-configured attributes (if any)
    style_parts = []
    for attr_name, attr_value in node.attributes.items():
        if attr_name in css_attributes:
            continue  # Handled via dynamic classes
        css_property = css_attributes.get(attr_name)
        if css_property:
            if attr_name == "color" and isinstance(attr_value, tuple):
                style_parts.append(f"{css_property}: rgb({attr_value[0]},{attr_value[1]},{attr_value[2]})")
            else:
                style_parts.append(f"{css_property}: {attr_value}")

    style_attr = f" style='{' '.join(style_parts)}'" if style_parts else ""

    # Handle leaf nodes
    if not node.children:
        if html_tag == "input":
            placeholder = generate_random_text(5)
            return " " * indent + f"<{html_tag}{class_attr}{style_attr} placeholder='{placeholder}'></{html_tag}>"
        elif html_tag == "select":
            return " " * indent + f"<{html_tag}{class_attr}{style_attr}>\n" + \
                " " * (indent + 2) + "<option value='' hidden selected>Select box</option>\n" + \
                " " * (indent + 2) + "<option value=''>Option 1</option>\n" + \
                " " * (indent + 2) + "<option value=''>Option 2</option>\n" + \
                " " * indent + f"</{html_tag}>"
        elif text_limit > 0:
            text = generate_random_text(text_limit)
            return " " * indent + f"<{html_tag}{class_attr}{style_attr}>{text}</{html_tag}>"
        return " " * indent + f"<{html_tag}{class_attr}{style_attr}></{html_tag}>"

    # Handle nodes with children
    children_html = "\n".join(
        generate_html(child, tag_mappings, used_classes, dynamic_css_rules, indent + 2) for child in node.children)
    return " " * indent + f"<{html_tag}{class_attr}{style_attr}>\n{children_html}\n" + " " * indent + f"</{html_tag}>"


def generate_html_template(html_content: str) -> str:
    """Wrap HTML content in a basic HTML template."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DSL Example</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
{html_content}
</body>
</html>"""

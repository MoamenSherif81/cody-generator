import os
import random
import string
from typing import Dict

from Compiler_V3.WebCodeGenerator.config import TagConfig, load_web_config_from_json
from Compiler_V3.WebCodeGenerator.layout import add_footer, add_header, add_side_nav
from Compiler_V3.models import ASTNode


def random_text(length: int) -> str:
    """Generate random text of specified length."""
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def handle_layout_node(node: ASTNode) -> (str, str):
    args = [arg for arg in node.attributes.get("args", []) if arg != ","]

    if isinstance(args, str):
        args = [args]
    color = node.attributes["color"] if "color" in node.attributes else "#f9f9f9"
    text_color = node.attributes["text_color"] if "text_color" in node.attributes else "#333"
    logo_color = node.attributes["logo_color"] if "logo_color" in node.attributes else "#222"

    title = node.attributes["title"] if "title" in node.attributes else "Logo"
    if node.tag == "header":
        return add_header(args=args, main_color=color, logo_text=title, text_color=text_color, logo_color=logo_color)
    elif node.tag == "footer":
        return add_footer(args=args, main_color=color, logo_text=title, text_color=text_color, logo_color=logo_color)
    elif node.tag == "side_nav":
        return add_side_nav(args=args, main_color=color, logo_text=title, text_color=text_color, logo_color=logo_color)
    else:
        return "", ""


def handle_color(value, css_prop) -> str:
    base = f"{css_prop} : "
    if isinstance(value, list) and len(value) == 3:
        base += f"rgb{tuple(value)};\n"
    elif len(value) == 1:
        base += f"{value[0]};\n"
    else:
        base += f"{value};\n"
    return base


def build_css_class(attrs: Dict[str, any], tag_css_attrs: Dict[str, str], base_classes: list[str]) -> (str, str):
    classes = " ".join(base_classes)
    if not attrs:
        return classes, ""
    attr_count = 0
    custom_class = random_text(6)
    css_block = f".{custom_class} " + "{\n"
    for key, value in attrs.items():
        key = key.replace('_', '-')
        if key in ["src", "text", "placeholder"]:
            continue

        if key in tag_css_attrs:
            css_prop = tag_css_attrs[key]
            if key == "color":
                css_block += handle_color(value, css_prop)
        else:
            css_block += f"{key}: "
            if isinstance(value, list):
                css_block += value[0]
            else:
                css_block += str(value)
            css_block += " ;\n"
        attr_count += 1
    css_block += "}\n"
    classes = classes + " " + custom_class
    if attr_count:
        return classes, css_block
    else:
        return classes, ""


def extract_text(node: ASTNode, attrs) -> str:
    if "text" in attrs:
        txt = attrs["text"]
        return f"{txt}"
    if "placeholder" in attrs and node.tag == "input":
        return f"{attrs["placeholder"]}"
    elif node.tag in ["input", "title", "button", "text"]:
        return random_text(6)
    return ""


def build_special_html(node: ASTNode, tag_conf: TagConfig) -> (str, str):
    """Handle special rendering for input and select_box with ids and options."""
    html_tag = tag_conf.htmlTag
    unique_id = random_text(8)
    class_names, css_code = build_css_class(node.attributes, tag_conf.cssAttributes, tag_conf.cssClasses)

    # Handle input element
    if node.tag == "input":
        placeholder = extract_text(node, node.attributes)
        return f'<{html_tag} class="{class_names}" id="{unique_id}" placeholder="{placeholder}"/>', css_code

    # Handle select_box element
    if node.tag == "select_box":
        # Use "options" attribute (should be a list of strings), or fallback to three dummy options
        options = node.attributes.get("options", ["Option 1", "Option 2", "Option 3"])
        options = [opt for opt in options if opt != ","]
        options_html = "\n".join([f'  <option value="{opt}">{opt}</option>' for opt in options])
        return f'<select class="{class_names}" id="{unique_id}">\n{options_html}\n</select>', css_code

    return "", ""  # fallback for unknown


def handle_image(node: ASTNode, tag_conf: TagConfig) -> (str, str):
    # Set default image source
    src = "https://community.softr.io/uploads/db9110/original/2X/7/74e6e7e382d0ff5d7773ca9a87e6f6f8817a68a6.jpeg"

    # Update the source if 'src' attribute exists in node
    if "src" in node.attributes:
        src = node.attributes["src"]
    class_names, css_code = build_css_class(node.attributes, tag_conf.cssAttributes, tag_conf.cssClasses)
    html = f'<{node.tag} src="{src}" class="{class_names}">'

    # Return the HTML with no additional CSS for now
    return html, css_code


def build_html_body(node: ASTNode, tag_map: Dict[str, TagConfig]) -> (str, str):
    html = ""
    css = ""
    if node.tag not in tag_map:
        raise Exception("Tag not mapped in config")
    tag_conf = tag_map[node.tag]
    if node.tag == "image":
        html2, css2 = handle_image(node, tag_conf)
        html += html2
        css += css2
        return html, css
    # Special handling for input and select_box
    if node.tag in ("input", "select_box"):
        retHtml, retCss = build_special_html(node, tag_conf)
        html += retHtml
        css += retCss
        return html, css

    html_tag = tag_conf.htmlTag
    class_names, css_code = build_css_class(node.attributes, tag_conf.cssAttributes, tag_conf.cssClasses)
    html += f'<{html_tag} class="{class_names}">'
    html += extract_text(node, node.attributes)
    for child in node.children:
        if child == ",":
            continue
        child_html, child_css = build_html_body(child, tag_map)
        html += child_html
        css_code += child_css
    html += f'</{html_tag}>'
    return html, css_code


def generate_html(ast_nodes: list, indent: int = 0) -> (str, str):
    """Compile DSL AST to HTML and CSS files."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "config.json")
    tag_map, opening_tag, closing_tag = load_web_config_from_json(config_path)
    html = ""
    css = ""
    for node in ast_nodes:
        # Handle layout node (header, footer, side-nav)
        if isinstance(node, ASTNode) and node.tag == "body":
            row_html, row_css = build_html_body(node, tag_map)
            html += row_html
            css += row_css
            continue
        if isinstance(node, ASTNode):
            html2, css2 = handle_layout_node(node)
            html += html2
            css += css2

    return html, css

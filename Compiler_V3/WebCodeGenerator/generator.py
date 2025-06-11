import os
import random
import string
from typing import Dict

from Compiler_V3.WebCodeGenerator.config import TagConfig, load_web_config_from_json
from Compiler_V3.WebCodeGenerator.layout.footer import add_footer
from Compiler_V3.WebCodeGenerator.layout.header import add_header
from Compiler_V3.WebCodeGenerator.layout.side_nav import add_side_nav
from Compiler_V3.models import ASTNode


def random_text(length: int) -> str:
    """Generate random text of specified length."""
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def handle_layout_node(node: ASTNode) -> (str, str):
    args = node.attributes["args"] if "args" in node.attributes else []
    if isinstance(args, str):
        args = [args]
    if node.tag == "header":
        return add_header(node.attributes["args"])
    elif node.tag == "footer":
        return add_footer(args)
    elif node.tag == "side_nav":
        return add_side_nav(args)
    else:
        return "", ""


def build_css_class(attrs: Dict[str, any], tag_css_attrs: Dict[str, str], base_classes: list[str]) -> (str, str):
    classes = " ".join(base_classes)
    if not attrs:
        return classes, ""
    attr_count = 0
    custom_class = random_text(6)
    css_block = f".{custom_class} " + "{\n"
    for key, value in attrs.items():
        if key == "text":
            continue
        if key in tag_css_attrs:
            css_prop = tag_css_attrs[key]
            if key == "color":
                css_block += f"{css_prop} : rgb{tuple(value)};\n"
            else:
                css_block += f"{css_prop} : {value};\n"
        else:
            css_block += f"{key} : {value[0]};\n"
        attr_count += 1
    css_block += "}\n"
    classes = classes + " " + custom_class
    if attr_count:
        return classes, css_block
    else:
        return classes, ""


def extract_text(attrs) -> str:
    if "text" in attrs:
        txt = attrs["text"][0]
        return f"{txt}"
    return ""


def build_special_html(node: ASTNode, tag_conf: TagConfig) -> (str, str):
    """Handle special rendering for input and select_box with ids and options."""
    html_tag = tag_conf.htmlTag
    unique_id = random_text(8)
    class_names, css_code = build_css_class(node.attributes, tag_conf.cssAttributes, tag_conf.cssClasses)

    # Handle input element
    if node.tag == "input":
        placeholder = extract_text(node.attributes)
        return f'<{html_tag} class="{class_names}" id="{unique_id}" placeholder="{placeholder}"/>', css_code

    # Handle select_box element
    if node.tag == "select_box":
        # Use "options" attribute (should be a list of strings), or fallback to three dummy options
        options = node.attributes.get("options", ["Option 1", "Option 2", "Option 3"])
        options_html = "\n".join([f'  <option value="{opt}">{opt}</option>' for opt in options])
        return f'<select class="{class_names}" id="{unique_id}">\n{options_html}\n</select>', css_code

    return "", ""  # fallback for unknown


def build_html_body(node: ASTNode, tag_map: Dict[str, TagConfig]) -> (str, str):
    html = ""
    css = ""
    if node.tag not in tag_map:
        raise Exception("Tag not mapped in config")
    tag_conf = tag_map[node.tag]

    # Special handling for input and select_box
    if node.tag in ("input", "select_box"):
        retHtml, retCss = build_special_html(node, tag_conf)
        html += retHtml
        css += retCss
        return html, css

    html_tag = tag_conf.htmlTag
    class_names, css_code = build_css_class(node.attributes, tag_conf.cssAttributes, tag_conf.cssClasses)
    html += f'<{html_tag} class="{class_names}">'
    html += extract_text(node.attributes)
    for child in node.children:
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
    is_side_nav_exist = False
    side_nav = None
    for node in ast_nodes:
        if isinstance(node, ASTNode):
            if node.tag == "side_nav":
                is_side_nav_exist = True
                side_nav = node
    if is_side_nav_exist:
        html += '<div class="main-content">'
    for node in ast_nodes:
        # Handle layout node (header, footer, side-nav)
        if isinstance(node, ASTNode):
            html2, css2 = handle_layout_node(node)
            html += html2
            css += css2
            if node.tag == "side_nav":
                continue
        # Handle rows (lists of ASTNode)
        if isinstance(node, list):
            for row_node in node:
                row_html, row_css = build_html_body(row_node, tag_map)
                html += row_html
                css += row_css
    if is_side_nav_exist:
        html+="</div>"
        html2,css2 = handle_layout_node(side_nav)
        html+=html2
        css += css2
    return html, css

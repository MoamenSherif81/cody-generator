from Compiler_V2.config import load_config
from Compiler_V2.linter import lint_and_format_dsl
from Compiler_V2.parser import tokenize, parse
from Compiler_V2.generator import generate_html, filter_css, generate_html_template, generate_css_template
from Compiler_V2.models import ASTNode
import os


def compile_dsl(dsl: str):
    """Compile DSL to HTML and CSS files."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_file = os.path.join(base_dir, "config.json")
    css_file = os.path.join(base_dir, "styles.css")

    tag_mappings, text_limits, colors, opening_tag, closing_tag = load_config(json_file)

    # Parse DSL
    tokens = tokenize(dsl, opening_tag, closing_tag)
    ast = parse(tokens, tag_mappings, opening_tag, closing_tag)

    # Generate HTML and collect used classes
    used_classes = set()
    html_content = generate_html(ast, tag_mappings, text_limits, used_classes, indent=2)

    # Wrap HTML in template
    wrapped_html = generate_html_template(html_content)
    css_content = filter_css(css_file, used_classes)
    wrapped_css = generate_css_template(css_content)
    return wrapped_html, wrapped_css


def lint_dsl(dsl: str) -> str:
    """Lint and reformat DSL code."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_file = os.path.join(base_dir, "config.json")
    css_file = os.path.join(base_dir, "styles.css")
    tag_mappings, text_limits, default_colors, opening_tag, closing_tag = load_config(json_file)
    return lint_and_format_dsl(dsl, tag_mappings, opening_tag, closing_tag)

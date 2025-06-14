from Compiler_V3 import validate_and_generate_ast
from Compiler_V3.WebCodeGenerator.clean_and_format_html_css import clean_and_format_html_css
from Compiler_V3.WebCodeGenerator.generator import generate_html
from Compiler_V3.WebCodeGenerator.layout.wrappers import html_wrapper, css_wrapper


def compile_to_web(dslCode: str):
    is_valid, ast_tree, error_message = validate_and_generate_ast(dslCode)
    if not is_valid:
        return "", "", error_message
    html, css = generate_html(ast_tree)
    html = html_wrapper(html)
    css = css_wrapper(css)
    formatted_html, _ = clean_and_format_html_css(html, css)
    return formatted_html, css, None

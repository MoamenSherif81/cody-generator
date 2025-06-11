from Compiler_V3 import validate_and_generate_ast,linter_formatter
from Compiler_V3.WebCodeGenerator.clean_and_format_html_css import clean_and_format_html_css
from Compiler_V3.WebCodeGenerator.generator import generate_html
from Compiler_V3.WebCodeGenerator.layout.wrappers import html_wrapper, css_wrapper


def compile_to_web(dslCode: str):
    is_valid, ast_tree, error_message = validate_and_generate_ast(dslCode)
    html, css = generate_html(ast_tree)
    html = html_wrapper(html)
    css = css_wrapper(css)
    formatted_html, _ = clean_and_format_html_css(html, css)

    # Write formatted HTML to file
    with open("/home/mohab/test/index.html", "w", encoding="utf-8") as html_file:
        html_file.write(formatted_html)

    # Write formatted CSS to file
    with open("/home/mohab/test/style.css", "w", encoding="utf-8") as css_file:
        css_file.write(css)


dsl = """
header<args=["Home","About Us","Services","Contact"]>
side_nav<args=["Home","Features","Pricing","FAQ"]>
row<testtag=("tag")>{
    box{
    title<text=("Welcome to our website"),color=(1,2,3)>,
    image<src=("https://via.placeholder.com/150")>,
    input<text=("Enter your name"),color=(23,2,232)>
    }
},
row{
    box{
        select_box<options=("Option 1", "Option 2", "Option 3")>,
        text<text=("Some text here")>
        }
    }
footer<args=["Privacy Policy","Terms of Service","Contact"]>
"""
compile_to_web(dsl)
print(linter_formatter(dsl))

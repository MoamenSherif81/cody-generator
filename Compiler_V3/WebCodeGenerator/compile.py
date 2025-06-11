from Compiler_V3 import validate_and_generate_ast
from Compiler_V3.WebCodeGenerator.clean_and_format_html_css import clean_and_format_html_css
from Compiler_V3.WebCodeGenerator.generator import generate_html
from Compiler_V3.WebCodeGenerator.wrappers import html_wrapper, css_wrapper


def compile_to_web(dslCode: str):
    is_valid, ast_tree, error_message = validate_and_generate_ast(dslCode)
    html, css = generate_html(ast_tree)
    html = html_wrapper(html)
    css = css_wrapper(css)
    formatted_html, _ = clean_and_format_html_css(html, css)
    print(formatted_html)
    print()
    print(css)
    # Write formatted HTML to file
    with open("/home/mohab/test/index.html", "w", encoding="utf-8") as html_file:
        html_file.write(formatted_html)

    # Write formatted CSS to file
    with open("/home/mohab/test/style.css", "w", encoding="utf-8") as css_file:
        css_file.write(css)

dsl = """
header<args=["title"]>
side_nav<>
row<testtag=("tag")>{
    box{
    title<text=("sdf"),color=(1,2,3)>,
    image,
    input<text=("enter your name"),color=(23,2,232)>
    }
},
row{
    box{
        select_box,
        text<text=("iam testing")>
        }
    }
footer<>
"""
compile_to_web(dsl)

"""
- first check if the ast node is header,footer,side-nav --> add template
- if list then it's rows 
    - loop over them one by one construct they html by recursion
- wrap them in html template
"""

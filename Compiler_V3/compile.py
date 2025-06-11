import os

from Compiler_V3 import validate_and_generate_ast
from Compiler_V3.config import load_config
from Compiler_V3.generator import generate_html

json_file = os.path.join(os.getcwd(), "config.json")
tag_mappings, opening_tag, closing_tag = load_config(json_file)
used_classes = set()
dynamic_css_rules = []
dsl="""
row{box{title<text=("sdf")>}}
"""
is_valid, ast_tree, error_message = validate_and_generate_ast(dsl)
print(ast_tree)
ast = ast_tree[0].children[0]
html_content = generate_html(ast, tag_mappings, used_classes, dynamic_css_rules, indent=2)
print(html_content)


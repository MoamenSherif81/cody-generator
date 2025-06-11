from Compiler_V3 import safe_compile_to_web, linter_formatter

dsl = """
row { box { title <color=(0,0,255), text=(Login)>, input <text=(Enter your username)>, input <text=(Enter your password)>, button <color=(52,199,89), text=(Login)> } } 
"""

print(linter_formatter(dsl))
html, css = (safe_compile_to_web(dsl))
print(html)

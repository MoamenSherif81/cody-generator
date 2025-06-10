dsl = """
row { box { title <color=(0,0,255), text=(Login)>, input <text=(Enter your username)>, input <text=(Enter your password)>, button <color=(52,199,89), text=(Login)> } } 
"""

from Compiler_V2 import compile_dsl, lint_dsl

print(lint_dsl(dsl))
html  ,css = (compile_dsl(dsl))
print(html)

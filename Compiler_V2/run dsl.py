dsl = """
row {
  box {
     input <text=(heool)>,
    select-box <text=(sdfsd)>

  }
}
"""

from Compiler_V2 import compile_dsl, lint_dsl

print(lint_dsl(dsl))
html  ,css = (compile_dsl(dsl))
print(html)

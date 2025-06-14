from Compiler_V3 import safe_compile_to_web, linter_formatter

dsl = """
'row <color=(0,122,255)> {box <color=(34,34,34),size=("24px")> {title <color=(245,245,245)>,text <color=(245,245,245)>},box <color=(0,122,255)>{select-box <color=(0,122,255)>}}'"""

print(linter_formatter(dsl))
html, css = (safe_compile_to_web(dsl))
print(html)

dsl = """
 row { box { title="What is your name?" }, box { input }, box { title="How old are you?", select-box }, box { title="What is your favorite color?", select-box }, box { title="Do you like coffee?", input }, box { title="Would you recommend this website?", button } } 
"""

from Compiler_V2 import compile_dsl

print(compile_dsl(dsl))

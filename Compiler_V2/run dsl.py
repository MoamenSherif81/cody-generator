dsl = """
{ 
    row <color=(230,230,250)> {
     box <color=(240,248,255)> { 
            title <color=(70,130,180)>
             }, 
     box <color=(240,248,255)> {
            input <placeholder='Username'>, 
            input <placeholder='Password'>,
             button <color=(70,130,180)>
              }
       } 
}
"""

from Compiler_V2 import compile_dsl

print(compile_dsl(dsl))

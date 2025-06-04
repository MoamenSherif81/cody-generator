from pydantic import BaseModel

from Compiler_V2 import is_compilable, compile_dsl, lint_dsl


class AnonymousCodeResponse(BaseModel):
    dsl: str
    html: str
    css: str

    @classmethod
    def from_dsl(cls, dsl: str):
        is_compilable(dsl)
        html, css = compile_dsl(dsl)
        dsl = lint_dsl(dsl)
        return cls(
            dsl=dsl,
            html=html,
            css=css
        )

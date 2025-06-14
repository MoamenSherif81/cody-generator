from pydantic import BaseModel

from Compiler_V3 import safe_compile_to_web, linter_formatter


class AnonymousCodeResponse(BaseModel):
    dsl: str
    html: str
    css: str

    @classmethod
    def from_dsl(cls, dsl: str):
        dsl = linter_formatter(dsl)
        print(dsl)
        html, css = safe_compile_to_web(dsl)
        return cls(
            dsl=dsl,
            html=html,
            css=css
        )

from PIL import Image
from fastapi import UploadFile
from Compiler_V2 import lint_dsl, compile_dsl
import io


def process_screenshot(uploaded_file: UploadFile):
    image_bytes = uploaded_file.file.read()
    image = Image.open(io.BytesIO(image_bytes))

    #todo: Placeholder: Call AI API to convert screenshot to DSL
    dsl = "row{box{text,input}},row{box{input,select-box},box{title},box{button}},row{box{text,input}}"

    html, css = compile_dsl(dsl)
    dsl = lint_dsl(dsl)
    return dsl, html, css

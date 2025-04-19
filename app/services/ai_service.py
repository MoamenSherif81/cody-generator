from typing import List

from fastapi import UploadFile

from Compiler_V2 import lint_dsl, compile_dsl
from Model.classes.models.config import IMAGE_SIZE
from Model.sampleFromImage import get_preprocessed_img_from_bytes, run_sampler
from app.services.shared_ai_state import model, sampler


def process_screenshot(uploaded_file: UploadFile):
    # Read the uploaded file bytes
    image_bytes = uploaded_file.file.read()

    # Preprocess the image in memory
    preprocessed_img = get_preprocessed_img_from_bytes(image_bytes, IMAGE_SIZE)
    # Call the sample function with the preprocessed image
    dsl = run_sampler(model, sampler, preprocessed_img)

    # Process the DSL
    html, css = compile_dsl(dsl)
    dsl = lint_dsl(dsl)
    return dsl, html, css


def process_screenshots(uploaded_files: List[UploadFile]):
    # Read the uploaded file bytes
    dsl = ""
    for img in uploaded_files:
        image_bytes = img.file.read()
        preprocessed_img = get_preprocessed_img_from_bytes(image_bytes, IMAGE_SIZE)
        temp = run_sampler(model, sampler, preprocessed_img)
        dsl += temp+","
    html, css = compile_dsl(dsl)
    dsl = lint_dsl(dsl)
    return dsl, html, css

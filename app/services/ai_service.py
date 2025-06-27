from typing import List

from fastapi import UploadFile, HTTPException

from Compiler_V3 import safe_compile_to_web
from Model.sampleFromImage import run_sampler, get_preprocessed_img_from_bytes, IMAGE_SIZE
# Assuming model and sampler are initialized elsewhere
from app.services.shared_ai_state import model, sampler  # Replace with your actual import


async def process_screenshots(uploaded_files: List[UploadFile]) -> str:
    """
    Process a list of uploaded images to generate DSL, HTML, and CSS.
    Reads file bytes once and processes them in memory.
    """
    dsl = ""
    print(dsl)

    for img in uploaded_files:
        # Validate content type
        if not img.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail=f"File {img.filename} is not an image")

        # Read file bytes
        image_bytes = await img.read()
        if not image_bytes:
            raise HTTPException(status_code=400, detail=f"File {img.filename} is empty")

        # Preprocess image in memory
        try:
            preprocessed_img = get_preprocessed_img_from_bytes(image_bytes, IMAGE_SIZE)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to process image {img.filename}: {str(e)}")

        # Run AI model to generate DSL
        try:
            temp_dsl = run_sampler(model, sampler, preprocessed_img)
            dsl += temp_dsl + ","
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"AI model failed for {img.filename}: {str(e)}")
    if not dsl:
        raise HTTPException(status_code=400, detail="No valid images processed")

    # Remove trailing comma and compile DSL
    dsl = dsl.rstrip(",")
    _, _ = safe_compile_to_web(dsl)
    return dsl
#
# def get_preprocessed_img_from_bytes(image_bytes: bytes, image_size: int) -> np.ndarray:
#     """
#     Preprocess an image from bytes without saving to disk.
#     """
#     try:
#         # Convert bytes to PIL Image
#         img = Image.open(io.BytesIO(image_bytes))
#         # Convert PIL Image to OpenCV format (BGR)
#         img = np.array(img)
#         if img.shape[-1] == 4:  # Handle RGBA images
#             img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
#         else:
#             img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
#
#         # Resize and preprocess
#         img = cv2.resize(img, (image_size, image_size))
#         img = img.astype('float32')
#         img /= 255
#         return img
#     except Exception as e:
#         raise ValueError(f"Failed to preprocess image: {str(e)}")

import io

import cv2
# sample_module.py
import numpy as np
from PIL import Image

from .classes.Sampler import Sampler
from .classes.Vocabulary import START_TOKEN, END_TOKEN
from .classes.models.config import CONTEXT_LENGTH
from .classes.models.pix2code_model import pix2code_model


def load_model_and_sampler(trained_weights_path, trained_model_name):
    meta_dataset = np.load(f"{trained_weights_path}/meta_dataset.npy", allow_pickle=True)
    input_shape = meta_dataset[0]
    output_size = meta_dataset[1]

    model = pix2code_model(input_shape, output_size, trained_weights_path)
    model.load(trained_model_name)

    sampler = Sampler(trained_weights_path, input_shape, output_size, CONTEXT_LENGTH)

    return model, sampler


def run_sampler(model, sampler, evaluation_img, search_method=0):
    if search_method == 0 or search_method == "greedy":
        result, _ = sampler.predict_greedy(model, np.array([evaluation_img]))
    else:
        beam_width = int(search_method)
        result, _ = sampler.predict_beam_search(
            model, np.array([evaluation_img]), beam_width=beam_width
        )

    result = result.replace(START_TOKEN, "").replace(END_TOKEN, "")
    return result


def get_preprocessed_img_from_bytes(image_bytes, image_size):
    """
    Preprocess an image from bytes without saving to disk.
    """
    # Convert bytes to a PIL Image
    img = Image.open(io.BytesIO(image_bytes))

    # Convert PIL Image to OpenCV format (BGR)
    img = np.array(img)
    if img.shape[-1] == 4:  # Handle RGBA images
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
    else:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Resize and preprocess as in the original get_preprocessed_img
    img = cv2.resize(img, (image_size, image_size))
    img = img.astype('float32')
    img /= 255
    return img


if __name__ == "__main__":
    print("sample image")

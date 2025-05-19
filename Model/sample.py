import sys
from os.path import basename, join, dirname

import numpy as np

from .Utils import Utils
from .classes.Sampler import Sampler
from .classes.Vocabulary import START_TOKEN, END_TOKEN
from .classes.models.config import CONTEXT_LENGTH, IMAGE_SIZE
from .classes.models.pix2code_model import pix2code_model


def sample(
        input_path,
        search_method=0,
        trained_weights_path=join(dirname(__file__), "..", "Extra", "bin"),
        trained_model_name="pix2code_model",
):
    meta_dataset = np.load(
        "{}/meta_dataset.npy".format(trained_weights_path), allow_pickle=True
    )
    input_shape = meta_dataset[0]
    output_size = meta_dataset[1]

    model = pix2code_model(input_shape, output_size, trained_weights_path)
    model.load(trained_model_name)

    sampler = Sampler(trained_weights_path, input_shape, output_size, CONTEXT_LENGTH)

    evaluation_img = Utils.get_preprocessed_img(input_path, IMAGE_SIZE)

    if search_method == 0:
        result, _ = sampler.predict_greedy(model, np.array([evaluation_img]))
        print("Result greedy: {}".format(result))
    else:
        beam_width = int(search_method)
        print("Search with beam width: {}".format(beam_width))
        result, _ = sampler.predict_beam_search(
            model, np.array([evaluation_img]), beam_width=beam_width
        )
        print("Result beam: {}".format(result))

    result = result.replace(START_TOKEN, "").replace(END_TOKEN, "")
    return result


if __name__ == "__main__":
    argv = sys.argv[1:]

    if len(argv) < 4:
        print("Error: not enough argument supplied:")
        print(
            "sample.py <trained weights path> <trained model name> <input image> <output path> <search method (default: greedy)>"
        )
        exit(0)
    else:
        trained_weights_path = argv[0]
        trained_model_name = argv[1]
        input_path = argv[2]
        output_path = argv[3]
        search_method = "greedy" if len(argv) < 5 else argv[4]

    file_name = basename(input_path)[: basename(input_path).find(".")]
    result = sample(
        input_path=input_path,
        trained_weights_path=trained_weights_path,
        trained_model_name=trained_model_name,
        search_method=search_method,
    )

    with open("{}/{}.gui".format(output_path, file_name), "w") as out_f:
        out_f.write(result)

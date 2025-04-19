import sys
import numpy as np
import os
from classes.dataset.Generator import Generator
from classes.dataset.Dataset import Dataset
from classes.Vocabulary import Vocabulary
from classes.models.config import BATCH_SIZE, IMAGE_SIZE, CONTEXT_LENGTH
from classes.models.pix2code_model import pix2code_model
from classes.Sampler import Sampler
from Utils import Utils
import tensorflow as tf

def token_level_accuracy(original, predicted):
    length_sum = 0
    match_sum = 0
    for idx, original_tokens in enumerate(original):
        predicted_tokens = predicted[idx]
        


def test_gready(testing_path, model, sampler):
    original = []
    predicted = []
    for f in os.listdir(testing_path):
        if f.find(".gui") != -1:
            gui = open("{}/{}".format(testing_path, f), "r")
            file_name = f[: f.find(".gui")]

            if os.path.isfile("{}/{}.png".format(testing_path, file_name)):
                img = Utils.get_preprocessed_img(
                    "{}/{}.png".format(testing_path, file_name), IMAGE_SIZE
                )
                original.append(gui)
                predicted.append(sampler.predict_greedy(model, np.array([img])))
    assert len(original) == len(predicted)
    print("greedy testing")


def run(
    testing_path, weights_path, model_name="pix2code_model", is_memory_intensive=False
):
    testing_dataset = Dataset()
    testing_dataset.load(testing_path, generate_binary_sequences=True)

    meta_dataset = np.load(
        "{}/meta_dataset.npy".format(weights_path), allow_pickle=True
    )

    input_shape = meta_dataset[0]
    output_size = meta_dataset[1]

    if not is_memory_intensive:
        testing_dataset.convert_arrays()
    else:
        testing_gui_paths, testing_img_paths = Dataset.load_paths_only(testing_path)

        voc = Vocabulary()
        voc.retrieve(weights_path)

        testing_steps_per_epoch = testing_dataset.size // BATCH_SIZE

        testing_generator = Generator.data_generator(
            voc,
            testing_gui_paths,
            testing_img_paths,
            batch_size=BATCH_SIZE,
            generate_binary_sequences=True,
        )

    model = pix2code_model(input_shape, output_size, weigths_path)
    model.load(model_name)

    if not is_memory_intensive:
        model.evaluate(
            testing_dataset.input_images,
            testing_dataset.partial_sequences,
            testing_dataset.next_words,
        )
    else:
        output_signature = (
            (
                tf.TensorSpec(
                    shape=(None, *(IMAGE_SIZE, IMAGE_SIZE), 3), dtype=tf.float32
                ),
                tf.TensorSpec(shape=(None, CONTEXT_LENGTH, voc.size), dtype=tf.float32),
            ),
            tf.TensorSpec(shape=(None, voc.size), dtype=tf.float32),
        )
        testing_dataset = tf.data.Dataset.from_generator(
            lambda: testing_generator, output_signature=output_signature
        )
        model.evaluate_generator(testing_dataset, steps=testing_steps_per_epoch)

    sampler = Sampler(weights_path, input_shape, output_size, CONTEXT_LENGTH)


if __name__ == "__main__":
    argv = sys.argv[1:]

    if len(argv) < 3:
        print("Error: not enough argument supplied:")
        print(
            "test.py <testing path> <weights path> <is memory intensive (default: 0)>"
        )
        exit(0)
    else:
        testing_path = argv[0]
        weigths_path = argv[1]
        use_generator = False if len(argv) < 3 else True if int(argv[2]) == 1 else False

    run(testing_path, weigths_path, is_memory_intensive=use_generator)

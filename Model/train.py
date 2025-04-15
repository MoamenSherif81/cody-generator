import sys
import numpy as np

from classes.dataset.Generator import Generator
from classes.dataset.Dataset import Dataset
from classes.Vocabulary import Vocabulary
from classes.models.config import BATCH_SIZE, IMAGE_SIZE, CONTEXT_LENGTH
from classes.models.pix2code_model import pix2code_model
import tensorflow as tf


def run(input_path, output_path, is_memory_intensive=False, pretrained_model=None):
    np.random.seed(1234)

    dataset = Dataset()
    dataset.load(input_path, generate_binary_sequences=True)
    dataset.save_metadata(output_path)
    dataset.voc.save(output_path)

    if not is_memory_intensive:
        dataset.convert_arrays()

        input_shape = dataset.input_shape
        output_size = dataset.output_size

        print(
            len(dataset.input_images),
            len(dataset.partial_sequences),
            len(dataset.next_words),
        )
        print(
            dataset.input_images.shape,
            dataset.partial_sequences.shape,
            dataset.next_words.shape,
        )
    else:
        gui_paths, img_paths = Dataset.load_paths_only(input_path)

        input_shape = dataset.input_shape
        output_size = dataset.output_size
        steps_per_epoch = dataset.size // BATCH_SIZE

        voc = Vocabulary()
        voc.retrieve(output_path)

        generator = Generator.data_generator(
            voc,
            gui_paths,
            img_paths,
            batch_size=BATCH_SIZE,
            generate_binary_sequences=True,
        )

    model = pix2code_model(input_shape, output_size, output_path)

    if pretrained_model is not None:
        model.model.load_weights(pretrained_model)

    if not is_memory_intensive:
        model.fit(dataset.input_images, dataset.partial_sequences, dataset.next_words)
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
        dataset = tf.data.Dataset.from_generator(
            lambda: generator, output_signature=output_signature
        )
        model.fit_generator(dataset, steps_per_epoch=steps_per_epoch)


if __name__ == "__main__":
    argv = sys.argv[1:]

    if len(argv) < 2:
        print("Error: not enough argument supplied:")
        print(
            "train.py <input path> <output path> <is memory intensive (default: 0)> <pretrained weights (optional)>"
        )
        exit(0)
    else:
        input_path = argv[0]
        output_path = argv[1]
        use_generator = False if len(argv) < 3 else True if int(argv[2]) == 1 else False
        pretrained_weigths = None if len(argv) < 4 else argv[3]

    run(
        input_path,
        output_path,
        is_memory_intensive=use_generator,
        pretrained_model=pretrained_weigths,
    )

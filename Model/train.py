import sys
import numpy as np

from classes.dataset.Generator import Generator
from classes.dataset.Dataset import Dataset
from classes.Vocabulary import Vocabulary
from classes.models.config import BATCH_SIZE, IMAGE_SIZE, CONTEXT_LENGTH
from classes.models.pix2code_model import pix2code_model
import tensorflow as tf


def run(
    training_path,
    validation_path,
    output_path,
    is_memory_intensive=False,
    pretrained_model=None,
):
    np.random.seed(1234)

    training_dataset = Dataset()
    training_dataset.load(training_path, generate_binary_sequences=True)
    training_dataset.save_metadata(output_path)
    training_dataset.voc.save(output_path)

    validation_dataset = Dataset()
    validation_dataset.load(validation_path, generate_binary_sequences=True)

    if not is_memory_intensive:
        training_dataset.convert_arrays()
        validation_dataset.convert_arrays()

        input_shape = training_dataset.input_shape
        output_size = training_dataset.output_size

        print(
            len(training_dataset.input_images),
            len(training_dataset.partial_sequences),
            len(training_dataset.next_words),
        )
        print(
            training_dataset.input_images.shape,
            training_dataset.partial_sequences.shape,
            training_dataset.next_words.shape,
        )
    else:
        training_gui_paths, training_img_paths = Dataset.load_paths_only(training_path)
        validation_gui_paths, validation_img_paths = Dataset.load_paths_only(
            validation_path
        )

        input_shape = training_dataset.input_shape
        output_size = training_dataset.output_size
        training_steps_per_epoch = training_dataset.size // BATCH_SIZE
        validation_steps_per_epoch = validation_dataset.size // BATCH_SIZE

        voc = Vocabulary()
        voc.retrieve(output_path)

        training_generator = Generator.data_generator(
            voc,
            training_gui_paths,
            training_img_paths,
            batch_size=BATCH_SIZE,
            generate_binary_sequences=True,
        )

        validation_generator = Generator.data_generator(
            voc,
            validation_gui_paths,
            validation_img_paths,
            batch_size=BATCH_SIZE,
            generate_binary_sequences=True,
        )

    model = pix2code_model(input_shape, output_size, output_path)

    if pretrained_model is not None:
        model.model.load_weights(pretrained_model, skip_mismatch=True)

    if not is_memory_intensive:
        model.fit(
            training_dataset.input_images,
            training_dataset.partial_sequences,
            training_dataset.next_words,
            (
                [validation_dataset.input_images, validation_dataset.partial_sequences],
                validation_dataset.next_words,
            ),
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
        training_dataset = tf.data.Dataset.from_generator(
            lambda: training_generator, output_signature=output_signature
        )
        validation_dataset = tf.data.Dataset.from_generator(
            lambda: validation_generator, output_signature=output_signature
        )
        model.fit_generator(
            training_dataset,
            steps_per_epoch=training_steps_per_epoch,
            validation_generator=validation_dataset,
            validation_steps=validation_steps_per_epoch
        )


if __name__ == "__main__":
    argv = sys.argv[1:]

    if len(argv) < 3:
        print("Error: not enough argument supplied:")
        print(
            "train.py <training path> <validation path> <output path> <is memory intensive (default: 0)> <pretrained weights (optional)>"
        )
        exit(0)
    else:
        training_path = argv[0]
        validation_path = argv[1]
        output_path = argv[2]
        use_generator = False if len(argv) < 4 else True if int(argv[3]) == 1 else False
        pretrained_weigths = None if len(argv) < 5 else argv[4]

    run(
        training_path,
        validation_path,
        output_path,
        is_memory_intensive=use_generator,
        pretrained_model=pretrained_weigths,
    )

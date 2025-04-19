import sys
import numpy as np
import os
from classes.dataset.Generator import Generator
from classes.dataset.Dataset import Dataset
from classes.Vocabulary import Vocabulary, START_TOKEN, END_TOKEN
from classes.models.config import BATCH_SIZE, IMAGE_SIZE, CONTEXT_LENGTH
from classes.models.pix2code_model import pix2code_model
from classes.Sampler import Sampler
from Utils import Utils
import tensorflow as tf
from tqdm import tqdm


def token_level_accuracy(original, predicted):
    length_sum = 0
    match_sum = 0
    for idx, original_tokens in enumerate(original):
        predicted_tokens = predicted[idx]
        length_sum += max(len(original_tokens), len(predicted_tokens))
        for i in range(min(len(original_tokens), len(predicted_tokens))):
            if original_tokens[i] == predicted_tokens[i]:
                match_sum += 1
    print("Token Level Accuracy {}".format(match_sum / length_sum))


def LCS_accuracy(original, predicted):
    length_sum = 0
    match_sum = 0
    for idx, original_tokens in enumerate(original):
        predicted_tokens = predicted[idx]
        length_sum += len(original_tokens)
        n = len(original_tokens)
        m = len(predicted_tokens)
        dp = []
        for idx_i in range(n):
            dp.append([])
            for idx_j in range(m):
                dp[idx_i].append(0)
                if original_tokens[idx_i] == predicted_tokens[idx_j]:
                    dp[idx_i][idx_j] = (
                        dp[idx_i - 1][idx_j - 1] + 1
                        if idx_i - 1 >= 0 and idx_j - 1 >= 0
                        else 1
                    )
                else:
                    dp[idx_i][idx_j] = max(
                        dp[idx_i - 1][idx_j] if idx_i - 1 >= 0 else 0,
                        dp[idx_i][idx_j - 1] if idx_j - 1 >= 0 else 0,
                    )
        match_sum += dp[n - 1][m - 1]
    print("LCS Accuracy {}".format(match_sum / length_sum))


def WER_accuracy(original, predicted):
    differance_sum = 0
    percentage = 0
    for idx, original_tokens in enumerate(original):
        predicted_tokens = predicted[idx]
        n = len(original_tokens)
        m = len(predicted_tokens)
        # max number, too lazy to add a variable, 5000 should be enough
        dp = []
        for idx_i in range(n + 1):
            dp.append([])
            for idx_j in range(m + 1):
                dp[idx_i].append(5000)
        dp[0][0] = 0
        for idx_i in range(n):
            for idx_j in range(m):
                if original_tokens[idx_i] == predicted_tokens[idx_j]:
                    dp[idx_i + 1][idx_j + 1] = min(
                        dp[idx_i + 1][idx_j + 1], dp[idx_i][idx_j]
                    )
                else:
                    dp[idx_i + 1][idx_j] = min(
                        dp[idx_i + 1][idx_j], dp[idx_i][idx_j] + 1
                    )
                    dp[idx_i][idx_j + 1] = min(
                        dp[idx_i][idx_j + 1], dp[idx_i][idx_j] + 1
                    )
                    dp[idx_i + 1][idx_j + 1] = min(
                        dp[idx_i + 1][idx_j + 1], dp[idx_i][idx_j] + 1
                    )
        differance_sum += dp[n][m]
        percentage += dp[n][m] / len(predicted_tokens)
    print(
        "WER(Word Error Rate) Accuracy (on average, how many tokens needs to be changed for predicred to be original) {}".format(
            differance_sum / len(original)
        )
    )
    print(
        "WER(Word Error Rate) Accuracy (on average, how much percentage of the predicred needs to be changed to be original) {}".format(
            percentage / len(original)
        )
    )


def test_gready(testing_path, model, sampler):
    print("greedy testing")
    original = []
    predicted = []

    gui_files = [f for f in os.listdir(testing_path) if f.endswith(".gui")]

    for f in tqdm(gui_files, desc="Processing GUI files"):
        with open(f"{testing_path}/{f}", "r") as file:
            contents = file.read()
            gui = Utils.tokenize_dsl(contents)

        file_name = f[: f.find(".gui")]

        img_path = f"{testing_path}/{file_name}.png"
        if os.path.isfile(img_path):
            img = Utils.get_preprocessed_img(img_path, IMAGE_SIZE)
            original.append(gui)
            predicted_gui, _ = sampler.predict_greedy(model, np.array([img]))
            predicted_gui = Utils.tokenize_dsl(
                predicted_gui.replace(START_TOKEN, "").replace(END_TOKEN, "")
            )
            predicted.append(predicted_gui)

    assert len(original) == len(predicted)
    token_level_accuracy(original, predicted)
    LCS_accuracy(original, predicted)
    WER_accuracy(original, predicted)
    print("------------------------------------------")


def test_beam_search(testing_path, beam_width, model, sampler):
    print("Beam search with k={} testing".format(beam_width))
    original = []
    predicted = []

    gui_files = [f for f in os.listdir(testing_path) if f.endswith(".gui")]

    for f in tqdm(gui_files, desc="Processing GUI files"):
        with open(f"{testing_path}/{f}", "r") as file:
            contents = file.read()
            gui = Utils.tokenize_dsl(contents)

        file_name = f[: f.find(".gui")]
        img_path = f"{testing_path}/{file_name}.png"

        if os.path.isfile(img_path):
            img = Utils.get_preprocessed_img(img_path, IMAGE_SIZE)
            original.append(gui)
            predicted_gui, _ = sampler.predict_beam_search(
                model, np.array([img]), beam_width=beam_width
            )
            predicted_gui = Utils.tokenize_dsl(
                predicted_gui.replace(START_TOKEN, "").replace(END_TOKEN, "")
            )
            predicted.append(predicted_gui)

    assert len(original) == len(predicted)
    token_level_accuracy(original, predicted)
    LCS_accuracy(original, predicted)
    WER_accuracy(original, predicted)
    print("------------------------------------------")


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
    # test_gready(testing_path, model, sampler)
    test_beam_search(testing_path, 3, model, sampler)
    test_beam_search(testing_path, 5, model, sampler)


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

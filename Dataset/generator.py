import os
import subprocess
import sys
from logging import exception


# TODO: Fix This class
class Generator:
    def __init__(
            self,
            folder_location="./",
            file_counter=0,
            rules_location=os.path.join(
                os.path.dirname(__file__), "..", "DSL", "dsl-rules.json"
            ),
            seed=281203,
    ):
        os.makedirs(os.path.join(folder_location, "input"), exist_ok=True)
        self.folder_location = os.path.join(folder_location, "input")
        self.rules_location = rules_location
        self.seed = seed
        self.file_counter = file_counter

    def basic_generate(self, num_samples):
        result = subprocess.run(
            [
                os.path.join(os.path.dirname(__file__), "basic_generator"),
                str(num_samples),
                self.folder_location,
                str(self.file_counter),
                self.rules_location,
                str(self.seed),
            ]
        )
        if result.returncode == 0:
            self.file_counter += num_samples
            print("Dataset generated!!")
            return True
        raise exception(result.stderr)

    def skewed_generate(self, num):
        pass

    def shuffle(self):
        pass


if __name__ == "__main__":
    # seed for random generator
    seed = int(sys.argv[1])
    # number of samples
    samples = int(sys.argv[2])
    # out_put directory
    output_directory = sys.argv[3]

    gen = Generator(output_directory, seed=seed)
    gen.basic_generate(samples)

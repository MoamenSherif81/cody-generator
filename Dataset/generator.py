import os
import subprocess
from logging import exception


class Generator:
    def __init__(self, folder_location="./", file_counter=0, rules_location="../DSL/dsl-rules.json", seed=281203):
        os.makedirs(folder_location + "Data", exist_ok=True)
        self.folder_location = folder_location + "Data/"
        self.rules_location = rules_location
        self.seed = seed
        self.file_counter = file_counter

    def basic_generate(self, num_samples):
        result = subprocess.run(["./basic_generator",str(num_samples), self.folder_location, str(self.file_counter), self.rules_location, str(self.seed)])
        if result.returncode == 0:
            self.file_counter += num_samples
            return True
        raise exception(result.stderr)



    def skewed_generate(self, num):
        pass

    def shuffle(self):
        pass


if __name__ == "__main__":
    gen = Generator()
    gen.basic_generate(5)


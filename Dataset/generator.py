import subprocess

class Generator:
    def __init__(self, folder_location="./", batch=1000, rules_location="../DSL/dsl-rules.json", seed=281203):
        self.folder_location = folder_location
        self.rules_location = rules_location
        self.seed = seed
        self.batch = batch
        self.file_counter = 0

    def basic_generate(self, num_samples):
        result = subprocess.run(["./basic_generator",str(num_samples), self.folder_location, str(self.batch), self.rules_location, str(self.seed)])
        # print("C++ output: ", result.stdout.strip())
        # print("C++ Error: ", result.stderr.strip())

    def skewed_generate(self, num):
        pass

    def shuffle(self):
        pass


if __name__ == "__main__":
    gen = Generator()
    gen.basic_generate(10)


import random


class TextGenerator:
    """
    A class to generate random sentences from a predefined list of words.
    """

    def __init__(self):
        """
        Initializes the TextGenerator with a predefined set of words.
        """
        self.words = [
            "apple", "banana", "car", "dog", "elephant", "fish", "grape", "house", "ice", "jungle",
            "kangaroo", "lemon", "mountain", "notebook", "orange", "penguin", "queen", "river", "sun",
            "tiger", "umbrella", "volcano", "whale", "xylophone", "yacht", "zebra", "ocean", "forest",
            "moon", "star", "cloud", "rain", "thunder", "lightning", "wind", "desert", "cactus", "valley",
            "hill", "bridge", "castle", "dragon", "wizard", "knight", "pirate", "treasure", "galaxy", "planet"
        ]

    def generate_sentence(self, length: int) -> str:
        """
        Generates a random sentence with the specified length.

        Args:
            length (int): The length of the sentence.

        Returns:
            str: A randomly generated sentence.
        """
        sentence = ' '.join(random.choices(self.words, k=length))
        return sentence.capitalize()[:length]

import json
import os.path

from Compiler.Tag import Tag


class Parser:
    """
    Class responsible for parsing the DSL code.
    """

    def __init__(self, code: str):
        """
        Initializes the Parser object.

        Args:
            code (str): The DSL code to be parsed.
        """
        self.code = code
        self.tags, self.tags_keys = self.load()

    def load(self) -> tuple[dict[str, Tag], list[str]]:
        """
        Loads tag data from JSON files and initializes Tag objects.

        Returns:
            tuple[dict[str, Tag], list[str]]: A dictionary of tag objects and a list of tag keys.
        """
        tags = {}
        tags_keys = []

        try:
            dsl_web_path = os.path.join(os.getcwd(),"dsl-web.json")
            with open(dsl_web_path, encoding="utf-8") as file:
                tokens = json.load(file)

            for token, value in tokens.items():
                if token in "}{":
                    continue
                tag = Tag(token, value)
                tags[token] = tag
                tags_keys.append(token)
            dsl_limits_path = os.path.join(os.getcwd(),"Dsl_txt_limit.json")
            with open(dsl_limits_path, encoding="utf-8") as file:
                size_limits = json.load(file)

            for token, limit in size_limits.items():
                if token in "}{":
                    continue
                if token in tags:
                    tags[token].text_size_limit = int(limit)

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading JSON files: {e}")

        return tags, tags_keys

    def parse_next(self, idx: int) -> tuple[Tag | None, int]:
        """
        Parses the next token from the code starting at the given index.

        Args:
            idx (int): The index to start parsing from.

        Returns:
            tuple[Tag | None, int]: The parsed Tag object (or None) and the new index.
        """
        current_token = ""
        n = len(self.code)

        for i in range(idx, n):
            ch = self.code[i]
            if ch in "{}":
                return Tag(ch, ""), i + 1
            if ch in " \n\t\r,":
                continue
            current_token += ch
            if current_token in self.tags_keys:
                return self.tags[current_token], i + 1

        return None, idx
ob = Parser("")

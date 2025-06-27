import os
import random

from Parser import Parser
from Tag import Tag
from TextGenerator import TextGenerator


class Node:
    """
    Represents a node in the syntax tree.
    """

    def __init__(self, tag: Tag):
        """
        Initializes a Node object.

        Args:
            tag (Tag): The tag associated with this node.
        """
        self.children = []
        self.tag = tag

    def __str__(self) -> str:
        return f"Node: {self.tag}"

    def __repr__(self) -> str:
        return self.__str__()

    def print_tree(self, level: int = 0):
        """
        Recursively prints the tree structure.

        Args:
            level (int, optional): The depth level of the tree. Defaults to 0.
        """
        print("  " * level + f"- {self.tag.tag_name}")
        for child in self.children:
            child.print_tree(level + 1)
        print("  " * level + f"- End-{self.tag.tag_name}")


class compiler:
    """
    Compiler class to parse and compile DSL code.
    """

    def __init__(self, savingPath: str):
        """
        Initializes the Compiler object.
        """
        self.parser = None
        self.root = None
        self.text_generator = TextGenerator()
        with open(
                os.path.join(os.path.dirname(__file__), "htmlTemplate.html"),
                "r",
                encoding="utf-8",
        ) as file:
            self.html_template = file.read()
        self.save_path = savingPath

    def compile(self, code: str, path: str = None):
        """
        Compiles the given DSL code.

        Args:
            code (str): The DSL code to compile.
            path (str, optional): The output path. Defaults to "".
        """
        self.parser = Parser(code)
        self.root = Node(Tag("body", "<body>[]</body>"))
        self.build_tree(0, self.root)
        compiled_code = self.build_code(self.root, 0)
        html_code = f"{self.html_template}{compiled_code}</html>"
        if path is not None:
            self.write_to_file("index.html", html_code)
        return html_code

    def write_to_file(self, file_name: str, text: str):
        """
        Writes compiled code to a file.

        Args:
            file_name (str): The name of the output file.
            text (str): The content to be written.
        """
        try:
            file_path = f"{self.save_path}/{file_name}"
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(text)
            # print("File written successfully!")
        except Exception as e:
            print(f"Error writing to file: {e}")

    def build_tree(self, idx: int, parent: Node) -> int:
        """
        Builds the syntax tree from the parser.

        Args:
            idx (int): The starting index for parsing.
            parent (Node): The parent node to attach children to.

        Returns:
            int: The updated index after building the tree.
        """
        while True:
            token, idx = self.parser.parse_next(idx)
            if token is None:
                break
            if token.tag_name not in "}{":
                node = Node(token)
                parent.children.append(node)
            if token.tag_name == "}":
                return idx
            if token.tag_name == "{":
                idx = self.build_tree(idx, node)
        return idx

    def build_code(self, node: Node, level: int = 0) -> str:
        """
        Recursively builds the code structure.

        Args:
            node (Node): The current node in the syntax tree.
            level (int, optional): The depth level for indentation. Defaults to 0.

        Returns:
            str: The generated code as a string.
        """
        indentation = "  " * level
        code = f"{indentation}{node.tag.open_tag}"
        if node.tag.tag_name in ["row", "box", "body"]:
            code += "\n"
        for child in node.children:
            code += self.build_code(child, level + 1)
        if node.tag.tag_name in ["row", "box", "body"]:
            code += indentation
        else:
            text_len = random.randint(
                int(0.5 * node.tag.text_size_limit), node.tag.text_size_limit
            )
            code += self.text_generator.generate_sentence(text_len)
        code += f"{node.tag.close_tag}\n"
        return code

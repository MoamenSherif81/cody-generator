from compiler import compiler
from Parser import Parser


def read_input_file(file_path: str) -> str:
    """Reads the DSL code from a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print("Error: File not found.")
        return ""
    except Exception as e:
        print(f"Error reading file: {e}")
        return ""


if __name__ == "__main__":
    file_path = "Compiler/dsl-example.gui"
    dsl_code = read_input_file(file_path)

    if dsl_code:
        compiler = compiler("Compiler/Generated")
        compiler.compile(dsl_code,"index.html")

import inspect
import json
import os

from json_repair import json_repair


def get_variable_name(variable):
    for name, value in inspect.currentframe().f_globals.items():
        if value == variable:
            return name
    return None


def parse_json(text):
    """
    Try to parse the JSON text. If it fails, try json_repair.
    """
    try:
        return json_repair.loads(text)
    except:
        return None


def load_json_data(json_file_path):
    """
    Load and parse the JSON data from a file.

    Args:
        json_file_path (str): The path to the JSON file.

    Returns:
        list: The parsed JSON data (if valid), or None if parsing fails.
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = file.read()
            return parse_json(data)
    except FileNotFoundError:
        print(f"File {json_file_path} not found.")
        # Create an empty file if it doesn't exist
        with open(json_file_path, 'w', encoding='utf-8') as file:
            file.write('[]')
        return []
    except json.JSONDecodeError:
        print(f"Error decoding the JSON file {json_file_path}.")
    except Exception as e:
        print(f"An error occurred while loading the file: {e}")
    return None


def write_json_data(json_file_path, data):
    """
    Write JSON data to a file.

    Args:
        json_file_path (str): The path to the JSON file.
        data (list): The JSON data to write to the file.
    """
    try:
        with open(json_file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")


def append_to_json_file(json_file_path, id, situation, dsl, lang):
    """
    Append a new record to an existing JSON file, keeping the file's original structure.
    The function assumes the JSON file contains an array of objects with 'id', 'situation', 'Dsl', and 'lang' keys.

    Args:
        json_file_path (str): The path to the JSON file.
        id: The ID for the new record.
        situation: The situation text (can be in any language including Arabic).
        dsl: The DSL data.
        lang: The language identifier.
    """
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(json_file_path)), exist_ok=True)

    # Load the existing data from the JSON file
    parsed_data = load_json_data(json_file_path)

    # Check if parsed_data is valid and a list
    if parsed_data is None:
        parsed_data = []  # Start with an empty list if there's an issue
    elif not isinstance(parsed_data, list):
        print("Error: The existing JSON structure must be a list of records.")
        parsed_data = []  # Reset to empty list if structure is wrong

    # Create the new record - no need to decode anything
    new_record = {
        "id": id,
        "situation": situation,  # Store as-is, without decoding
        "dsl": dsl,
        "lang": lang
    }
    # Append the new record to the data
    parsed_data.append(new_record)

    # Write the updated data back to the JSON file
    write_json_data(json_file_path, parsed_data)

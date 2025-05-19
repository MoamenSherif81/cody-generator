from random import shuffle

from LLM.Utils import write_json_data
from Utils import load_json_data

# Define path variable
file_path = "FT_Dataset/situations.json"

# Load data from the JSON file
data = load_json_data(file_path)
idx = 0

# Process each item in the data
for i in data:
    try:
        Dsl = str(i['dsl']).strip()
        if Dsl and Dsl[0] == '{' and Dsl[-1] == '}':
            i['dsl'] = Dsl[1:-1]  # Remove the first and last characters
        print(Dsl)
        idx += 1
    except KeyError:
        print(f"Error: 'dsl' key not found in record at index {idx}")
        idx += 1
    except Exception as e:
        print(f"An unexpected error occurred at index {idx}: {e}")
        idx += 1

# Shuffle the data
shuffle(data)

# Add an 'id' to each item
id = 1
for i in data:
    i['id'] = id
    id += 1

# Write the modified data back to the file
write_json_data(file_path, data)

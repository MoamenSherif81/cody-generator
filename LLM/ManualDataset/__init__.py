import math
import os
import random
import json
import gspread
from dotenv import load_dotenv
from LLM.Scheme.AnswerQuestion import AnswerQuestion
from tqdm import tqdm  # Added tqdm import

# Load environment variables
load_dotenv()

def load_google_credentials():
    """Load Google credentials and sheet ID from environment variables."""
    sheet_id = os.getenv("SHEET_ID", "")
    secret_file_name = os.getenv("GOOGLE_SECRET_KEY_FILE", "")

    if not sheet_id or not secret_file_name:
        raise ValueError("Sheet ID or Secret Key file path not provided in environment variables.")

    cred_path = os.path.join(os.getcwd(), secret_file_name)
    gc = gspread.service_account(filename=cred_path)
    sh = gc.open_by_key(sheet_id)
    return sh

def fetch_records_from_sheets(sheets, sh):
    """Fetch records from the specified sheets in the Google Sheets document."""
    records = []
    for lang in sheets:
        worksheet = sh.worksheet(lang)
        records.extend(worksheet.get_all_records())
    return records

def shuffle_data(data, seed_value):
    """Shuffle data with a fixed seed value."""
    random.seed(seed_value)
    random.shuffle(data)

def prepare_finetuning_data(records, dsl_rules_path, system_message):
    """Prepare the data for LLM fine-tuning with progress bar."""
    llm_finetunning_data = []
    with open(dsl_rules_path, 'r') as file:
        dsl_rules = file.read()

    for rec in tqdm(records, desc="Processing records"):  # Added tqdm progress bar
        llm_finetunning_data.append({
            "system": system_message,
            "instruction": "\n".join([
                "# Story:",
                rec["Situation"],
                "# Task:",
                "generate the dsl for the provided situation",
                f"# Output Scheme:{json.dumps(AnswerQuestion.model_json_schema(), ensure_ascii=False)}",
                "# Output JSON:",
                "```json"
            ]),
            "input": "",
            "output": "\n".join([
                "```json",
                f'{{"dsl": {json.dumps(rec["Dsl"], ensure_ascii=False)}}}',
                "```"
            ]),
            "history": []
        })

    return llm_finetunning_data

def split_data(data, train_ratio):
    """Split data into training and validation datasets."""
    total = len(data)
    train_size = math.floor(total * train_ratio)
    eval_size = total - train_size
    train_ds = data[:train_size]
    eval_ds = data[train_size:]
    return train_ds, eval_ds

def save_data(train_ds, eval_ds, output_path):
    """Save training and evaluation datasets to JSON files."""
    os.makedirs(output_path, exist_ok=True)
    with open(os.path.join(output_path, "train.json"), "w", encoding="utf8") as dest:
        json.dump(train_ds, dest, ensure_ascii=False, default=str)
    with open(os.path.join(output_path, "val.json"), "w", encoding="utf8") as dest:
        json.dump(eval_ds, dest, ensure_ascii=False, default=str)

def main():
    sheets = ["Arabic", "English", "ArabicAndEnglish", "Egyptian"]
    seed_value = 42
    output_path = os.path.join(os.getcwd(), "LLM", "ManualDataset", "Output")
    train_ratio = .70
    # Load Google Sheets credentials and fetch records
    sh = load_google_credentials()
    records = fetch_records_from_sheets(sheets, sh)

    # Shuffle data
    shuffle_data(records, seed_value)

    # Prepare fine-tuning data
    json_rules_path = "LLM/Queries/DSL-Rules.json"
    system_message = "\n".join([
        "You are a professional Frontend Developer that can generate webpage using our own custom DSL.",
        f"You have to Generate response JSON {json.dumps(AnswerQuestion.model_json_schema(), ensure_ascii=False)} according to the Pydantic details.",
        "Follow the provided `Task` by the user and the `Output Scheme` to generate the `Output JSON`.",
        "Do not generate any introduction or conclusion."
    ])
    llm_finetunning_data = prepare_finetuning_data(records, json_rules_path, system_message)

    # Shuffle fine-tuning data again
    shuffle_data(llm_finetunning_data, seed_value)

    # Split data into training and validation sets
    train_ds, eval_ds = split_data(llm_finetunning_data, train_ratio)

    # Save datasets to JSON files
    save_data(train_ds, eval_ds, output_path)

    print(f"Training data saved to {os.path.join(output_path, 'train.json')}")
    print(f"Validation data saved to {os.path.join(output_path, 'val.json')}")

if __name__ == "__main__":
    main()
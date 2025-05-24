import os
import time
import gspread
import threading
from typing import List, Dict
from apscheduler.schedulers.background import BackgroundScheduler
from google.auth.exceptions import GoogleAuthError
from googleapiclient.errors import HttpError

records: Dict[str, List[List[str]]] = {}

records_lock = threading.Lock()

def add_record(sheet_id: str, record: List[str]) -> None:
    """
    Add a record to the specific sheet ID in the records dictionary.
    Ensure that no other thread can modify the dictionary during this operation.
    """
    with records_lock:
        if sheet_id not in records:
            records[sheet_id] = []
        records[sheet_id].append(record)
        print(f"Added record to {sheet_id}: {record}")

# Push records to Google Sheets
def push_to_google_sheets() -> None:
    """
    Push the stored records in the 'records' dictionary to the Google Sheets.
    Use a lock to prevent other operations from modifying records while flushing.
    """
    total_records = 0
    sheet_id = os.getenv("SHEET_ID", "")
    secret_file_name = os.getenv("GOOGLE_SECRET_KEY_FILE", "")

    if not sheet_id or not secret_file_name:
        raise ValueError("Sheet ID or Secret Key file path not provided in environment variables.")
    cred_path = os.path.join(os.getcwd(), secret_file_name)

    try:
        gc = gspread.service_account(filename=cred_path)
        sh = gc.open_by_key(sheet_id)
        with records_lock:
            # Iterate over records and push them to respective sheets
            for sheet_name, rows in records.items():
                if not rows:  # Skip empty sheets
                    continue

                try:
                    worksheet = sh.worksheet(sheet_name)
                    worksheet.append_rows(rows)
                    total_records += len(rows)
                    print(f"Pushed {len(rows)} records to sheet: {sheet_name}")
                except gspread.exceptions.WorksheetNotFound:
                    print(f"Worksheet {sheet_name} not found in Google Sheets.")
                except HttpError as e:
                    print(f"HTTP error occurred while pushing records to {sheet_name}: {e}")
                except Exception as e:
                    print(f"Error pushing records to {sheet_name}: {e}")

            records.clear()

        print(f"{total_records} records pushed to Google Sheets at {time.strftime('%Y-%m-%d %H:%M:%S')}")

    except GoogleAuthError as auth_error:
        print(f"Authentication failed: {auth_error}")
    except Exception as general_error:
        print(f"An unexpected error occurred while pushing to Google Sheets: {general_error}")

def start_scheduler() -> BackgroundScheduler:
    """
    Starts the APScheduler and sets up the background job.
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(push_to_google_sheets, 'interval', seconds=60)  # Push records to Google Sheets every 60 seconds
    scheduler.start()
    print("Scheduler started to push records every 60 seconds.")
    return scheduler

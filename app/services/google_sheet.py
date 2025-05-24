import os
from datetime import datetime

import gspread


def _init():
    sheetId = os.getenv("SHEET_ID", "")
    secretFileName = os.getenv("GOOGLE_SECRET_KEY_FILE", "")
    credPath = os.path.join(os.getcwd(), secretFileName)
    gc = gspread.service_account(filename=credPath)
    sh = gc.open_by_key(sheetId)
    return sh

def append_log(userName: str, log: str):
    sh = _init()
    worksheet = sh.worksheet("Logs")
    timestamp = datetime.now().strftime("%A, %Y-%m-%d %H:%M:%S")
    worksheet.append_row([timestamp, userName, log])


def append_record(username, aiModel, situation, dsl, lang):
    sh = _init()
    worksheet = sh.worksheet(lang)
    timestamp = datetime.now().strftime("%A, %Y-%m-%d %H:%M:%S")
    worksheet.append_row([username, aiModel, timestamp, situation, dsl])

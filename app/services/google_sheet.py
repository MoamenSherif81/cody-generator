import os
from datetime import datetime

import gspread


def append_log(userName: str, log: str):
    credPath = os.path.join(os.getcwd(), "app", "llm-gp-data.json")
    gc = gspread.service_account(filename=credPath)
    sh = gc.open_by_key("1Y17nNQ5WUPU5c3QnwPyaGaQvo2jgCVCXGANhrJ_OnQ8")
    worksheet = sh.worksheet("Logs")
    timestamp = datetime.now().strftime("%A, %Y-%m-%d %H:%M:%S")
    worksheet.append_row([timestamp, userName, log])


def append_record(username, aiModel, situation, dsl, lang):
    credPath = os.path.join(os.getcwd(), "app", "llm-gp-data.json")
    gc = gspread.service_account(filename=credPath)
    sh = gc.open_by_key("1Y17nNQ5WUPU5c3QnwPyaGaQvo2jgCVCXGANhrJ_OnQ8")
    worksheet = sh.worksheet(lang)
    timestamp = datetime.now().strftime("%A, %Y-%m-%d %H:%M:%S")
    worksheet.append_row([username, aiModel, timestamp, situation, dsl])

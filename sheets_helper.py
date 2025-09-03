import os
import json
from typing import Dict, Any, List
from datetime import datetime

import gspread
from google.oauth2.service_account import Credentials

from questions import QUESTIONS

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def get_client():
    sa_json_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not sa_json_path or not os.path.exists(sa_json_path):
        raise FileNotFoundError("GOOGLE_SERVICE_ACCOUNT_JSON topilmadi yoki yo'li xato.")
    creds = Credentials.from_service_account_file(sa_json_path, scopes=SCOPES)
    client = gspread.authorize(creds)
    return client

def get_worksheet(spreadsheet_url: str, sheet_name: str):
    client = get_client()
    sh = client.open_by_url(spreadsheet_url)
    try:
        ws = sh.worksheet(sheet_name)
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(title=sheet_name, rows=1000, cols=50)
        # Sarlavhalar
        headers = ["timestamp", "user_id", "username", "full_name", "category", "answers_json", "videos_json"]
        ws.append_row(headers, value_input_option="RAW")
    return ws

def append_submission(spreadsheet_url: str, sheet_name: str, answers: Dict[str, Any]):
    ws = get_worksheet(spreadsheet_url, sheet_name)
    row: List[str] = []
    for quistion in QUESTIONS[sheet_name]:
        row.append(answers[quistion["text"]])
    ws.append_row(row, value_input_option="RAW")
    return True
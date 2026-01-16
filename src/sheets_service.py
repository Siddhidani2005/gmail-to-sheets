# src/sheets_service.py
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from .config import SHEETS_SCOPES, SPREADSHEET_ID, SHEET_NAME
import socket

socket.setdefaulttimeout(30)


def get_sheets_service():
    """Authenticate and return Google Sheets service"""
    creds = Credentials.from_service_account_file(
        "service_account.json",
        scopes=SHEETS_SCOPES
    )
    service = build(
        "sheets",
        "v4",
        credentials=creds,
        cache_discovery=False
    )
    return service


def get_existing_message_ids(service):
    """
    Fetch existing message IDs from the first column to avoid duplicates.
    Returns a set of IDs.
    """
    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!A2:A"  # Assuming first row is header
        ).execute()

        values = result.get("values", [])
        return {row[0] for row in values if row}
    except Exception:
        # Return empty set if sheet is empty or API fails
        return set()


def append_row(service, values):
    """Append a single row to Google Sheets"""
    try:
        service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!A:E",  # Columns A-E, adjust if needed
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body={"values": [values]}
        ).execute()
    except Exception as e:
        raise RuntimeError(f"Failed to append row: {e}")


def append_rows(service, rows):
    """Append multiple rows to Google Sheets in a single API call"""
    if not rows:
        return

    try:
        service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!A:E",  # Columns A-E, adjust if needed
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body={"values": rows}
        ).execute()
    except Exception as e:
        raise RuntimeError(f"Failed to append rows: {e}")

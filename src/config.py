# config.py

# OAuth scopes (USED DURING LOGIN)
OAUTH_SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/spreadsheets"
]

# Gmail API scopes (logical grouping)
GMAIL_SCOPES = OAUTH_SCOPES

# Google Sheets API scopes (logical grouping)
SHEETS_SCOPES = OAUTH_SCOPES

# OAuth files
GMAIL_CREDENTIALS_FILE = "credentials/credentials.json"
GMAIL_TOKEN_FILE = "credentials/token.json"

# Google Sheet details
SPREADSHEET_ID = "sheet_id"
SHEET_NAME = "Sheet1"

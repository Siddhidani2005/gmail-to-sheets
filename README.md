# Gmail to Sheets

A Python application that automatically syncs unread emails from Gmail to a Google Sheet, extracting key information and organizing it for easy reference.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Google Cloud Configuration](#google-cloud-configuration)
  - [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)

## Features

- **Automatic Email Sync**: Fetches unread emails from your Gmail inbox
- **Duplicate Prevention**: Tracks synced emails to avoid duplicates
- **Email Parsing**: Extracts sender, subject, date, and body content
- **Google Sheets Integration**: Appends parsed emails to a Google Sheet
- **Read Status Management**: Automatically marks processed emails as read
- **Batch Processing**: Efficiently appends multiple emails in a single API call
- **Error Logging**: Comprehensive logging for debugging and monitoring

## Architecture

### System Design

```
┌─────────────────────────────────────────────────────────────┐
│                    Gmail to Sheets App                       │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐      ┌───────────────┐                   │
│  │   Gmail      │      │  Google       │                   │
│  │   API        │──────│  Sheets API   │                   │
│  └──────────────┘      └───────────────┘                   │
│       ▲                        ▲                             │
│       │                        │                             │
│  ┌────┴────────────────────────┴──────┐                    │
│  │    Application Services             │                    │
│  ├─────────────────────────────────────┤                    │
│  │  • gmail_service.py                 │                    │
│  │  • sheets_service.py                │                    │
│  │  • email_parser.py                  │                    │
│  │  • main.py                          │                    │
│  └─────────────────────────────────────┘                    │
│                                                               │
│  ┌─────────────────────────────────────┐                    │
│  │   Configuration & Credentials        │                    │
│  ├─────────────────────────────────────┤                    │
│  │  • config.py                        │                    │
│  │  • credentials/credentials.json     │                    │
│  │  • credentials/token.json           │                    │
│  │  • service_account.json             │                    │
│  └─────────────────────────────────────┘                    │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Module Breakdown

#### `src/main.py`
The orchestrator module that:
- Initializes Gmail and Sheets services
- Fetches existing message IDs to prevent duplicates
- Retrieves unread emails from Gmail
- Parses each email to extract data
- Appends new emails to Google Sheets
- Marks emails as read in Gmail

#### `src/gmail_service.py`
Handles Gmail API interactions:
- **`get_gmail_service()`**: Authenticates with OAuth 2.0 and returns Gmail service instance
- **`fetch_unread_emails(service)`**: Retrieves all unread emails from the inbox
- **`mark_as_read(service, msg_id)`**: Marks an email as read by removing the UNREAD label

#### `src/sheets_service.py`
Manages Google Sheets API interactions:
- **`get_sheets_service()`**: Authenticates using service account credentials
- **`get_existing_message_ids(service)`**: Retrieves all message IDs already in the sheet to prevent duplicates
- **`append_rows(service, rows)`**: Appends multiple rows to the sheet in a single batch API call

#### `src/email_parser.py`
Extracts email data:
- **`parse_email(service, msg_id)`**: Fetches full email and extracts From, Subject, Date, and Content
- **`_get_plain_text(payload)`**: Recursively extracts plain text from email payload, handling multipart messages

#### `src/config.py`
Central configuration file containing:
- OAuth scopes for Gmail and Sheets APIs
- Credential file paths
- Google Sheet ID and sheet name

## Setup

### Prerequisites

- Python 3.7+
- A Google Account
- A Google Cloud Project with Gmail and Sheets APIs enabled
- Google Sheets API credentials (OAuth 2.0)
- Google Sheets API service account key

### Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd gmail-to-sheets
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   ```

   On Windows:
   ```bash
   venv\Scripts\activate
   ```

   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Google Cloud Configuration

#### Step 1: Create a Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the **Gmail API** and **Google Sheets API**

#### Step 2: Create OAuth 2.0 Credentials (for Gmail)
1. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID"
2. Choose "Desktop application"
3. Download the JSON file as `credentials/credentials.json`

#### Step 3: Create Service Account Credentials (for Google Sheets)
1. Go to "Credentials" → "Create Credentials" → "Service Account"
2. Create the service account and generate a key (JSON format)
3. Save the JSON file as `service_account.json` in the project root
4. Share your target Google Sheet with the service account email address

#### Step 4: Set Up the Google Sheet
1. Create a new Google Sheet
2. Add headers in the first row: `Message ID | From | Subject | Date | Content | FetchedAt`
3. Copy the Sheet ID from the URL and update `SPREADSHEET_ID` in `src/config.py`

### Configuration

Edit `src/config.py` to customize:

```python
SPREADSHEET_ID = "your-sheet-id-here"  # Google Sheet ID from URL
SHEET_NAME = "Sheet1"                   # Name of the sheet tab
GMAIL_CREDENTIALS_FILE = "credentials/credentials.json"  # OAuth credentials
GMAIL_TOKEN_FILE = "credentials/token.json"  # Token (auto-created on first run)
```

## Usage

### Running the Application

Execute the sync with:

```bash
python -m src.main
```

Or from the project root:

```bash
python src/main.py
```

### First Run

On the first run, you'll be prompted to authorize the application:
1. A browser window opens
2. Sign in with your Google Account
3. Grant the requested permissions
4. The token is automatically saved to `credentials/token.json`

### Subsequent Runs

The application uses the saved token, so no authorization is needed on subsequent runs (unless the token expires).

### Output

The application logs all actions:
```
2026-01-16 10:30:45,123 - INFO - Starting Gmail to Sheets sync...
2026-01-16 10:30:46,456 - INFO - Found 5 existing emails in the sheet.
2026-01-16 10:30:47,789 - INFO - Fetched 3 unread emails from Gmail.
2026-01-16 10:30:48,012 - INFO - Successfully appended 3 emails to Google Sheets.
2026-01-16 10:30:48,345 - INFO - Gmail to Sheets sync completed.
```

## Project Structure

```
gmail-to-sheets/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── service_account.json         # Google Sheets service account key
├── credentials/
│   ├── credentials.json         # Gmail OAuth 2.0 credentials (user-provided)
│   └── token.json               # Gmail OAuth token (auto-generated)
├── src/
│   ├── __pycache__/             # Python cache
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # Application entry point
│   ├── config.py                # Configuration and constants
│   ├── gmail_service.py         # Gmail API wrapper
│   ├── sheets_service.py        # Google Sheets API wrapper
│   └── email_parser.py          # Email parsing utilities
└── proof/                       # Test/proof artifacts
```

## How It Works

### Sync Flow

```
1. Initialize Services
   ├─ Gmail service (OAuth 2.0)
   └─ Sheets service (Service Account)

2. Load Existing Data
   └─ Fetch all message IDs from Google Sheet
      (Used to prevent duplicate syncing)

3. Fetch Unread Emails
   └─ Query Gmail API for messages with UNREAD label in INBOX

4. Process Each Email
   ├─ Check if already synced (via message ID)
   ├─ Parse email content (From, Subject, Date, Body)
   ├─ Mark as read in Gmail
   └─ Add to batch for sheet insertion

5. Append to Google Sheet
   ├─ Batch insert all new emails
   └─ Each row: [ID, From, Subject, Date, Content, FetchedAt]

6. Complete
   └─ Log results and exit
```

### Duplicate Prevention

The application maintains data integrity by:
1. Fetching all existing message IDs from the sheet's first column
2. Checking each unread email against this set
3. Skipping any already-synced emails
4. Still marking skipped emails as read in Gmail

### API Efficiency

- **Batch Inserts**: Appends multiple rows in a single API call instead of one per email
- **Lazy Parsing**: Only parses emails that haven't been synced before
- **Pagination**: Handles large email lists by paginating through Gmail results

## Troubleshooting

### Common Issues

**"Authentication failed"**
- Delete `credentials/token.json` and run again to re-authenticate
- Ensure `credentials/credentials.json` exists in the credentials folder

**"Spreadsheet not found"**
- Verify `SPREADSHEET_ID` in `config.py` is correct
- Ensure the service account email has access to the sheet

**"No emails synced"**
- Check that you have unread emails in Gmail
- Verify Gmail API is enabled in Google Cloud Console
- Check the logs for specific error messages

**"Permission denied on sheets"**
- Share the Google Sheet with the service account email address
- Ensure the service account has Editor permissions

## Dependencies

- `google-api-python-client`: Google API client library
- `google-auth-oauthlib`: OAuth 2.0 authentication for user credentials
- `google-auth-httplib2`: HTTP transport for authentication
- `google-auth`: Google authentication library

All dependencies are listed in `requirements.txt`.

⚠ Limitations
Processes only unread emails from Inbox.
Attachments are not supported.
Only plain text is saved (HTML formatting lost).

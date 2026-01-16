# src/main.py
import logging
from .gmail_service import get_gmail_service, fetch_unread_emails, mark_as_read
from .sheets_service import get_sheets_service, append_row, get_existing_message_ids
from .email_parser import parse_email

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():
    logging.info("Starting Gmail to Sheets sync...")

    # Authenticate services
    gmail = get_gmail_service()
    sheets = get_sheets_service()

    # Get existing Message IDs to avoid duplicates
    existing_ids = get_existing_message_ids(sheets)
    logging.info(f"Found {len(existing_ids)} existing emails in the sheet.")

    # Fetch unread emails
    messages = fetch_unread_emails(gmail)
    if not messages:
        logging.info("No new unread emails.")
        return

    logging.info(f"Fetched {len(messages)} unread emails from Gmail.")

    rows_to_append = []

    for msg in messages:
        msg_id = msg.get("id")
        if not msg_id:
            continue

        if msg_id in existing_ids:
            logging.info(f"Email {msg_id} already exists. Marking as read.")
            mark_as_read(gmail, msg_id)
            continue

        try:
            data = parse_email(gmail, msg_id)
        except Exception as e:
            logging.error(f"Failed to parse email {msg_id}: {e}")
            continue

        # Prepare row for Google Sheets
        rows_to_append.append([
            msg_id,
            data.get("From", ""),
            data.get("Subject", ""),
            data.get("Date", ""),
            data.get("Content", "")
        ])

        # Mark email as read
        mark_as_read(gmail, msg_id)

    # Append all new emails at once
    if rows_to_append:
        try:
            for row in rows_to_append:
                append_row(sheets, row)
            logging.info(f"Successfully appended {len(rows_to_append)} emails to Google Sheets.")
        except Exception as e:
            logging.error(f"Failed to append rows to Google Sheets: {e}")
    else:
        logging.info("No new emails to append.")

    logging.info("Gmail to Sheets sync completed.")


if __name__ == "__main__":
    main()

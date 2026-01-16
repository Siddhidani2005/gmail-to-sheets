import base64
from email.utils import parsedate_to_datetime

def parse_email(service, msg_id):
    msg = service.users().messages().get(
        userId="me", id=msg_id, format="full"
    ).execute()

    headers = msg["payload"]["headers"]
    data = {"From": "", "Subject": "", "Date": "", "Content": ""}

    for h in headers:
        if h["name"] in data:
            data[h["name"]] = h["value"]

    data["Date"] = str(parsedate_to_datetime(data["Date"]))

    parts = msg["payload"].get("parts", [])
    for part in parts:
        if part["mimeType"] == "text/plain":
            body = part["body"].get("data", "")
            data["Content"] = base64.urlsafe_b64decode(body).decode("utf-8")
            break

    return data

import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from crewai.tools import tool
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from scopes import SCOPES

def authenticate_gmail():
    creds = None
    token_path = "token.json"

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Token expired, refreshing...")
            creds.refresh(Request())
        else:
            print("🔑 No valid token, performing new authentication...")
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=8080)

        with open(token_path, "w") as token_file:
            token_file.write(creds.to_json())

    return creds

@tool
def send_email(to_email: str, subject: str, body: str):
    """Send email using Gmail API."""
    try:
        creds = authenticate_gmail()
        service = build("gmail", "v1", credentials=creds)

        message = MIMEText(body)
        message["to"] = to_email
        message["subject"] = subject
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        send_message = (
            service.users()
            .messages()
            .send(userId="me", body={"raw": raw_message})
            .execute()
        )

        return f"Email sent successfully to {to_email}, Message ID: {send_message['id']}"

    except Exception as e:
        return f"Failed to send email: {e}"

import os
import sys
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from typing import Optional
from googleapiclient.discovery import build
from crewai.tools import tool
from scopes import SCOPES

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def get_credentials():
    creds = None
    # Jika token sudah ada, gunakan token yang ada
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # Jika tidak ada atau token expired, lakukan autentikasi ulang
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=8080)
        # Simpan token agar bisa digunakan lagi
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds

# Inisialisasi service Google Calendar
creds = get_credentials()
service = build("calendar", "v3", credentials=creds)

@tool("create_event")
def create_event(summary: str, start_time: str, end_time: str, description: Optional[str] = ""):
    """create new event on Google Calendar"""
    event = {
        "summary": summary,
        "description": description,
        "start": {"dateTime": start_time, "timeZone": "Asia/Jakarta"},
        "end": {"dateTime": end_time, "timeZone": "Asia/Jakarta"},
    }
    event = service.events().insert(calendarId="primary", body=event).execute()
    return f"Event created: {event.get('htmlLink')}"

@tool("update_event")
def update_event(event_id: str, summary: Optional[str] = None, start_time: Optional[str] = None, end_time: Optional[str] = None, description: Optional[str] = None):
    """update the event based on event_id"""
    event = service.events().get(calendarId="primary", eventId=event_id).execute()
    if summary:
        event["summary"] = summary
    if description:
        event["description"] = description
    if start_time:
        event["start"]["dateTime"] = start_time
    if end_time:
        event["end"]["dateTime"] = end_time
    updated_event = service.events().update(calendarId="primary", eventId=event_id, body=event).execute()
    return f"Event updated: {updated_event.get('htmlLink')}"

@tool("delete_event")
def delete_event(event_id: str):
    """delete the event based on event_id"""
    deleted_event = service.events().delete(calendarId="primary", eventId=event_id).execute()
    return f"Event deleted: {deleted_event.get('htmlLink')}"

import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_calendar_service():

    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)


def register_event(service, match):

    event = {
        "summary": f"{match['home']} vs {match['away']}",
        "description": match.get("competition", ""),
        "start": {
            "dateTime": match["start"].isoformat(),
            "timeZone": "Asia/Tokyo",
        },
        "end": {
            "dateTime": match["end"].isoformat(),
            "timeZone": "Asia/Tokyo",
        },
    }

    return service.events().insert(calendarId="primary", body=event).execute()


def register_matches(service, matches):

    links = []

    for match in matches:
        event = register_event(service, match)
        links.append(event.get("htmlLink"))

    return links
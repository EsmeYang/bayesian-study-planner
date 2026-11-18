
from datetime import datetime, timedelta
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from src.decision import ACTIONS


SCOPES = [
    "https://www.googleapis.com/auth/calendar.events"
]

BASE_DIR = Path(__file__).resolve().parent.parent
CREDENTIALS_FILE = BASE_DIR / "credentials.json"
TOKEN_FILE = BASE_DIR / "token.json"


def create_study_event(action, start_time):
    """Create a Google Calendar event preview."""

    if action not in ACTIONS:
        raise ValueError(f"Unknown action: {action}")

    if not isinstance(start_time, datetime):
        raise TypeError("start_time must be a datetime object")

    if start_time.tzinfo is None or start_time.utcoffset() is None:
        raise ValueError("start_time must include a timezone")

    hours = ACTIONS[action]["hours"]

    # A rest day does not require a study session.
    if hours == 0:
        return None

    end_time = start_time + timedelta(hours=hours)

    return {
        "summary": f"BayesStudy - {action}",
        "description": (
            "Study session recommended by BayesStudy. "
            "This is based on a prototype Bayesian "
            "expected utility decision model."
        ),
        "start": {
            "dateTime": start_time.isoformat(),
        },
        "end": {
            "dateTime": end_time.isoformat(),
        },
    }


def get_calendar_service():
    """Authenticate with Google Calendar using OAuth 2.0."""

    credentials = None

    if TOKEN_FILE.exists():
        credentials = Credentials.from_authorized_user_file(
            str(TOKEN_FILE),
            SCOPES,
        )

    if (
        credentials
        and credentials.expired
        and credentials.refresh_token
    ):
        credentials.refresh(Request())

    if not credentials or not credentials.valid:
        if not CREDENTIALS_FILE.exists():
            raise FileNotFoundError(
                "credentials.json was not found. "
                "Download OAuth Desktop credentials "
                "from Google Cloud Console."
            )

        flow = InstalledAppFlow.from_client_secrets_file(
            str(CREDENTIALS_FILE),
            SCOPES,
        )

        credentials = flow.run_local_server(port=0)

    TOKEN_FILE.write_text(credentials.to_json())

    return build(
        "calendar",
        "v3",
        credentials=credentials,
    )


def add_event_to_calendar(event):
    """Insert a confirmed event into the primary Google Calendar."""

    if event is None:
        raise ValueError("Cannot add an empty calendar event")

    service = get_calendar_service()

    created_event = (
        service.events()
        .insert(
            calendarId="primary",
            body=event,
        )
        .execute()
    )

    return created_event


def main():
    """Preview a study session and request confirmation."""

    action = "Light Review"

    # Example: November 20, 2026, 2 PM Pacific Standard Time.
    # Change this to your preferred date and time.
    start_time = datetime.fromisoformat(
        "2026-11-20T14:00:00-08:00"
    )

    event = create_study_event(action, start_time)

    print("\nBayesStudy - Google Calendar Integration")
    print("---------------------------------------")

    if event is None:
        print("Rest Day: no study session required.")
        return

    print("Calendar Event Preview")
    print("Title:", event["summary"])
    print("Start:", event["start"]["dateTime"])
    print("End:", event["end"]["dateTime"])

    confirmation = input(
        "\nAdd this event to Google Calendar? (yes/no): "
    ).strip().lower()

    if confirmation != "yes":
        print("Cancelled. No calendar event was created.")
        return

    created_event = add_event_to_calendar(event)

    print("\nGoogle Calendar event created successfully!")
    print("Event link:", created_event.get("htmlLink"))


if __name__ == "__main__":
    main()

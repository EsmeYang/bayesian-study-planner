
from datetime import datetime, timedelta, timezone

import pytest

from src.calendar_integration import create_study_event


START_TIME = datetime(
    2026,
    11,
    20,
    14,
    0,
    tzinfo=timezone(timedelta(hours=-8)),
)


def test_intensive_study_duration():
    event = create_study_event(
        "Intensive Study",
        START_TIME,
    )

    start = datetime.fromisoformat(
        event["start"]["dateTime"]
    )
    end = datetime.fromisoformat(
        event["end"]["dateTime"]
    )

    assert end - start == timedelta(hours=5)


def test_light_review_duration():
    event = create_study_event(
        "Light Review",
        START_TIME,
    )

    start = datetime.fromisoformat(
        event["start"]["dateTime"]
    )
    end = datetime.fromisoformat(
        event["end"]["dateTime"]
    )

    assert end - start == timedelta(hours=1)


def test_rest_day_has_no_event():
    event = create_study_event(
        "Rest Day",
        START_TIME,
    )

    assert event is None


def test_event_has_required_fields():
    event = create_study_event(
        "Light Review",
        START_TIME,
    )

    assert "summary" in event
    assert "description" in event
    assert "start" in event
    assert "end" in event


def test_invalid_action():
    with pytest.raises(ValueError):
        create_study_event(
            "Unknown Action",
            START_TIME,
        )


def test_timezone_required():
    naive_start = datetime(
        2026, 11, 20, 14, 0
    )

    with pytest.raises(ValueError):
        create_study_event(
            "Light Review",
            naive_start,
        )

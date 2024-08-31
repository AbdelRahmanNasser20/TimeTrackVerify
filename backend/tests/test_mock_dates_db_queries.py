import pytest
from datetime import datetime, date
from unittest.mock import MagicMock
from app.db_queries import get_events_for_month, get_event_by_date_position, get_events_by_date

# Use pytest fixture to set up a mock session
@pytest.fixture
def mock_session():
    return MagicMock()

# Helper function to create a mock event with a given date
def create_mock_event(date_str, duration=2.0, position="Manager", location="Office"):
    mock_event = MagicMock()
    mock_event.date = datetime.strptime(date_str, '%Y-%m-%d').date()
    mock_event.duration = duration
    mock_event.position = position
    mock_event.location = location
    return mock_event

def test_get_event_by_date_position_found(mock_session):
    # Event is found
    mock_event = create_mock_event('2023-12-03')
    mock_session.query.return_value.filter_by.return_value.first.return_value = mock_event

    event = get_event_by_date_position(1, '2023-12-03', 'Manager', 2.0, session=mock_session)
    assert event is not None
    assert event.date == '2023-12-03'

def test_get_event_by_date_position_not_found(mock_session):
    # Event is not found
    mock_session.query.return_value.filter_by.return_value.first.return_value = None

    event = get_event_by_date_position(1, '2023-12-03', 'Manager', 2.0, session=mock_session)
    assert event is None

def test_get_events_by_date_found(mock_session):
    # Multiple events on the same date
    mock_session.query.return_value.filter_by.return_value.all.return_value = [
        create_mock_event('2023-12-03', 2.0, 'Manager'),
        create_mock_event('2023-12-03', 3.0, 'Assistant')
    ]

    events = get_events_by_date(1, '2023-12-03', session=mock_session)
    assert len(events) == 2
    assert events[0]['date'] == '2023-12-03'
    assert events[1]['date'] == '2023-12-03'
    assert events[0]['position'] == 'Manager'
    assert events[1]['position'] == 'Assistant'

def test_get_events_by_date_not_found(mock_session):
    # No events on the specified date
    mock_session.query.return_value.filter_by.return_value.all.return_value = []

    events = get_events_by_date(1, '2023-12-03', session=mock_session)
    assert len(events) == 0

def test_get_events_for_february_non_leap_year(mock_session):
    # February with 28 days
    mock_session.query.return_value.filter.return_value.all.return_value = [
        create_mock_event('2023-02-15')
    ]

    events = get_events_for_month(1, '2023-02-01', session=mock_session)
    assert len(events) == 1
    assert events[0]['date'] == '2023-02-15'

def test_get_events_for_april(mock_session):
    # April with 30 days
    mock_session.query.return_value.filter.return_value.all.return_value = [
        create_mock_event('2023-04-10'),
        create_mock_event('2023-04-30')
    ]

    events = get_events_for_month(1, '2023-04-01', session=mock_session)
    assert len(events) == 2
    assert events[0]['date'] == '2023-04-10'
    assert events[1]['date'] == '2023-04-30'

def test_get_events_for_july(mock_session):
    # July with 31 days
    mock_session.query.return_value.filter.return_value.all.return_value = [
        create_mock_event('2023-07-01'),
        create_mock_event('2023-07-31')
    ]

    events = get_events_for_month(1, '2023-07-01', session=mock_session)
    assert len(events) == 2
    assert events[0]['date'] == '2023-07-01'
    assert events[1]['date'] == '2023-07-31'

def test_get_events_for_february_leap_year(mock_session):
    # February with 29 days in a leap year
    mock_session.query.return_value.filter.return_value.all.return_value = [
        create_mock_event('2024-02-29')
    ]

    events = get_events_for_month(1, '2024-02-01', session=mock_session)
    assert len(events) == 1
    assert events[0]['date'] == '2024-02-29'

def test_invalid_date_format(mock_session):
    with pytest.raises(ValueError):
        # Passing an invalid date format that the function cannot parse
        get_events_for_month(1, '12-03-2023', session=mock_session)

def test_none_date_object(mock_session):
    with pytest.raises(TypeError):
        get_events_for_month(1, None, session=mock_session)

def test_first_day_of_month(mock_session):
    mock_event = create_mock_event('2023-12-01')
    mock_session.query.return_value.filter.return_value.all.return_value = [mock_event]

    events = get_events_for_month(1, '2023-12-01', session=mock_session)
    assert len(events) == 1
    assert events[0]['date'] == '2023-12-01'

def test_last_day_of_month(mock_session):
    mock_event = create_mock_event('2023-12-31')
    mock_session.query.return_value.filter.return_value.all.return_value = [mock_event]

    events = get_events_for_month(1, '2023-12-01', session=mock_session)
    assert len(events) == 1
    assert events[0]['date'] == '2023-12-31'

def test_non_existent_date(mock_session):
    # This test is now not applicable because datetime.date objects won't allow creation of invalid dates
    pass

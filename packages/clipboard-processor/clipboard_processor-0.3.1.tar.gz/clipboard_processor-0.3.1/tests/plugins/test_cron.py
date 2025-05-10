import pytest

from clipboard_processor.plugins.cron import CronPlugin


@pytest.mark.full_installation
@pytest.mark.parametrize('input_data, expected_output', [
    ('* 2 3 * *', ['Every minute, between 02:00 and 02:59, on day 3 of the month']),
    ('0 5 ? * MON-FRI *', ['At 05:00, Monday through Friday']),
    ('* * *', []),
    ('yearly', []),
])
def test_cron(input_data, expected_output):
    assert CronPlugin().process(input_data) == expected_output


@pytest.mark.full_installation
def test_is_available():
    assert CronPlugin.is_available() is True


@pytest.mark.minimal_installation
def test_is_not_available():
    assert CronPlugin.is_available() is False

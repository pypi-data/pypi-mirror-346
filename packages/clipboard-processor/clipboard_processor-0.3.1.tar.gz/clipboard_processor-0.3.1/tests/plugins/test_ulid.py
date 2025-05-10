import pytest

from clipboard_processor.plugins import UlidPlugin


@pytest.mark.full_installation
def test_valid_ulid():
    plugin = UlidPlugin()
    assert plugin.process('01ARZ3NDEKTSV4RRFFQ69G5FAV') == ['ULID at 2016-07-30 23:54:10.259000Z']


@pytest.mark.full_installation
def test_invalid_ulid():
    plugin = UlidPlugin()
    assert plugin.process('01ARZ3NDEKTSV4RRFFQ69G5FAv') == []


@pytest.mark.full_installation
def test_is_available():
    assert UlidPlugin.is_available() is True


@pytest.mark.minimal_installation
def test_is_not_available():
    assert UlidPlugin.is_available() is False

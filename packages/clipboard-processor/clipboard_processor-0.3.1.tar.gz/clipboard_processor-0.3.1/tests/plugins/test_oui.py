import pytest
from clipboard_processor.plugins.oui import OuiPlugin


@pytest.mark.full_installation
@pytest.mark.parametrize('input_data, expected_output', [
    ('B8:27:EB:12:34:56', ['Raspberry Pi Foundation (B8-27-EB)']),
    ('b8-27-eb-12-34-56', ['Raspberry Pi Foundation (B8-27-EB)']),
    ('b827eb123456', ['Raspberry Pi Foundation (B8-27-EB)']),
    ('b8-27-eb', ['Raspberry Pi Foundation (B8-27-EB)']),
    ('b827eb', ['Raspberry Pi Foundation (B8-27-EB)']),
    ('b8:27:eb', ['Raspberry Pi Foundation (B8-27-EB)']),
    ('01:23:45', []),  # not registered
    ('b8/27/eb', []),  # invalid format
    ('b8)7', []),  # invalid format
    ('b827eb12345', []),  # invalid format
    ('b827eb1234567', []),  # invalid format
    ('b827eb12345600', []),  # invalid format
    ('b827eb_', []),  # invalid format
    ('0b827eb', []),  # invalid format
])
def test_oui(input_data, expected_output):
    assert OuiPlugin().process(input_data) == expected_output


@pytest.mark.full_installation
def test_is_available():
    assert OuiPlugin.is_available() is True


@pytest.mark.minimal_installation
def test_is_not_available():
    assert OuiPlugin.is_available() is False

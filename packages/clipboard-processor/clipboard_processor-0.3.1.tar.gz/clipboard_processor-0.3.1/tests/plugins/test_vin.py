import pytest

from clipboard_processor.plugins import VinPlugin


@pytest.mark.full_installation
def test_valid_vin():
    plugin = VinPlugin()
    assert plugin.process('JF2SHADC3DG417185') == ['Country: Japan', 'Manufacturer: Subaru', 'Region: Asia',
                                                   'Years: 2013, 1983']
    assert plugin.process('JF2SHADC3DG417000') == ['Country: Japan', 'Manufacturer: Subaru', 'Region: Asia',
                                                   'Years: 2013, 1983', 'Checksum invalid!']


@pytest.mark.full_installation
def test_invalid_vin():
    plugin = VinPlugin()
    assert plugin.process('JF2SHADC3DG41700') == []  # too short
    assert plugin.process('JF2SHADC3DG4170001') == []  # too long


@pytest.mark.full_installation
def test_is_available():
    assert VinPlugin.is_available() is True


@pytest.mark.minimal_installation
def test_is_not_available():
    assert VinPlugin.is_available() is False

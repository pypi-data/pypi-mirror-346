import pytest
from clipboard_processor.plugins.hex import HexPlugin


@pytest.mark.parametrize('input_data, expected_output', [
    ('74657374', ['test']),
    ('c3a6e280a6', ['æ…']),
    ('C3A6E280A6', ['æ…']),
    ('2a2A2024052220', []),  # not printable
    ('7465737g', []),  # not hex
    ('7465737', []),  # not hex
])
def test_hex(input_data, expected_output):
    assert HexPlugin().process(input_data) == expected_output

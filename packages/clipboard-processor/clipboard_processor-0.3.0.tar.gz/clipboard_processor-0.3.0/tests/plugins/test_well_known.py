import pytest

from clipboard_processor.plugins.well_known import WellKnownPlugin


@pytest.mark.parametrize('input_data, expected_output', [
    ('4b825dc642cb6eb9a060e54bf8d69288fbee4904', ['git empty tree object hash (sha1)']),
    ('6ef19b41225c5369f1c104d45d8d85efa9b057b53b14b4b9b939dd74decc5321', ['git empty tree object hash (sha256)']),
    ('foo', []),
])
def test_well_known(input_data, expected_output):
    assert WellKnownPlugin().process(input_data) == expected_output

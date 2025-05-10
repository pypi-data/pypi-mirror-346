from clipboard_processor.plugins import Base64Plugin

VALID_BASE64 = 'dGVzdA=='
DECODED_BASE64 = 'test'
INVALID_BASE64 = 'dGVzdA='


def test_valid_base64():
    plugin = Base64Plugin()
    assert plugin.process(VALID_BASE64) == [DECODED_BASE64]


def test_invalid_base64():
    plugin = Base64Plugin()
    assert plugin.process(INVALID_BASE64) == []

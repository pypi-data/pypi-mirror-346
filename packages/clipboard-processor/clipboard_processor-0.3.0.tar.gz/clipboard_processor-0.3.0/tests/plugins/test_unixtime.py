from clipboard_processor.plugins import UnixTimePlugin


def test_valid_unix_times():
    plugin = UnixTimePlugin()
    assert plugin.process('1610152804') == ['2021-01-09 00:40:04Z']
    assert plugin.process('1610152804123') == ['2021-01-09 00:40:04.123000Z']
    assert plugin.process('1610152804123456') == ['2021-01-09 00:40:04.123456Z']


def test_invalid_unix_times():
    plugin = UnixTimePlugin()
    assert plugin.process('yesterday') == []
    assert plugin.process('16101528041234567') == []
    assert plugin.process('161015280412') == []
    assert plugin.process('161015280412345678') == []
    assert plugin.process('1610152804123456789') == []

import pytest

from clipboard_processor.plugins import JwtPlugin

VALID_JWT = ('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2dnZWRJbkFzIjoiYWRtaW4iLCJpYXQiOjE0MjI3Nzk2Mzh9.'
             'gzSraSYS8EXBxLN_oWnFSRgCzcmJmMjLiuyu5CSpyHI=')


@pytest.mark.full_installation
def test_valid_jwt():
    plugin = JwtPlugin()
    assert plugin.process(VALID_JWT) == ['{\n  "loggedInAs": "admin",\n  "iat": 1422779638\n}']


@pytest.mark.full_installation
def test_valid_jwt_with_bearer():
    plugin = JwtPlugin()
    assert plugin.process('Bearer ' + VALID_JWT) == ['{\n  "loggedInAs": "admin",\n  "iat": 1422779638\n}']


@pytest.mark.full_installation
def test_invalid_jwt():
    plugin = JwtPlugin()
    assert plugin.process(VALID_JWT[0:20]) == []


@pytest.mark.full_installation
def test_is_available():
    assert JwtPlugin.is_available() is True


@pytest.mark.minimal_installation
def test_is_not_available():
    assert JwtPlugin.is_available() is False

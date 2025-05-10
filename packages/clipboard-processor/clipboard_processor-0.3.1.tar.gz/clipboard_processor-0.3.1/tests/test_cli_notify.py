import os
import signal
import time

import pytest

from test_cli import SLEEP_STARTUP_SECONDS, SLEEP_PROCESSING_SECONDS, BASE64_DATA, BASE64_DECODED
from util import run_cli, copy_to_clipboard

try:
    import dbusmock.pytest_fixtures
    pytest_plugins = "dbusmock.pytest_fixtures"
    dbusmock_available = True
except ModuleNotFoundError:
    dbusmock_available = False


@pytest.fixture(autouse=True)
def empty_clipboard():
    copy_to_clipboard('')


@pytest.mark.skipif(not dbusmock_available, reason="dbusmock not available")
def test_cli_with_notification_and_stdout(dbus_notifications_mock):
    # when
    with run_cli('-o', 'notify', '-o', 'stdout') as proc:
        time.sleep(SLEEP_STARTUP_SECONDS)
        copy_to_clipboard(BASE64_DATA)
        time.sleep(SLEEP_PROCESSING_SECONDS)
        proc.send_signal(signal.SIGINT)

        output = proc.stdout.readlines()

    # then
    assert proc.returncode == 0
    assert BASE64_DATA in output[0]  # ensure clipboard has been processed, so we can expect a notification

    os.set_blocking(dbus_notifications_mock.stdout.fileno(), False)
    dbus_mock_output = b''.join(dbus_notifications_mock.stdout.readlines()).decode('utf-8')
    assert 'Notify "clipboard-processor"' in dbus_mock_output
    assert BASE64_DATA in dbus_mock_output
    assert BASE64_DECODED in dbus_mock_output


@pytest.fixture
def dbus_notifications_mock(dbusmock_session):
    assert dbusmock_session
    print(dbusmock_session.address)
    with dbusmock.SpawnedMock.spawn_with_template("notification_daemon") as server:
        yield server

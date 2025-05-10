import signal
import subprocess
import time

from test_cli import SLEEP_STARTUP_SECONDS, BASE64_DATA, SLEEP_PROCESSING_SECONDS, BASE64_DECODED
from util import run_cli


def test_cli_with_xclip_primary():
    # given
    subprocess.run(['xclip', '-selection', 'primary'], input='', encoding='utf-8', check=True)

    # when
    with run_cli('--input', 'xclip-primary', '--output', 'stdout') as proc:
        time.sleep(SLEEP_STARTUP_SECONDS)
        subprocess.run(['xclip', '-selection', 'primary'], input=BASE64_DATA, encoding='utf-8', check=True)
        time.sleep(SLEEP_PROCESSING_SECONDS)
        proc.send_signal(signal.SIGINT)

        output = proc.stdout.readlines()
        error = proc.stderr.readlines()

    # then
    assert proc.returncode == 0
    assert BASE64_DATA in output[0]
    assert output[1].strip() == BASE64_DECODED
    assert len(error) == 0


def test_cli_with_xclip_primary_handles_non_utf8_data_gracefully(tmp_path):
    # given
    data_file = tmp_path / 'data.bin'
    data_file.write_bytes(b'\xFF\xFE\xFD\xFC\xFB\xFA\xF9\xF8')  # type: ignore

    # when
    with run_cli('--input', 'xclip-primary', '--output', 'stdout') as proc:
        time.sleep(SLEEP_STARTUP_SECONDS)
        subprocess.run(['xclip', '-selection', 'primary', data_file], encoding='utf-8', check=True)
        time.sleep(SLEEP_PROCESSING_SECONDS)

        proc.send_signal(signal.SIGINT)

        output = proc.stdout.readlines()
        error = proc.stderr.readlines()

    assert proc.returncode == 0
    assert len(output) == 0
    assert len(error) == 0

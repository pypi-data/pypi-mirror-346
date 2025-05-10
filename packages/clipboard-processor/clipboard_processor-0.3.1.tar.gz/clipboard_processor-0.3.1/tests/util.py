import subprocess
from contextlib import contextmanager

import pyperclip


@contextmanager
def run_cli(*args):
    with subprocess.Popen(['clipboard-processor'] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          encoding='utf-8') as proc:
        yield proc


def copy_to_clipboard(data: str):
    pyperclip.copy(data)

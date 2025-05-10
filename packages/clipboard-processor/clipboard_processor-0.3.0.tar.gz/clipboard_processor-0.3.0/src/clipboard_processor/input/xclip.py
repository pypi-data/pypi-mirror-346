import shutil
import subprocess

from clipboard_processor.input._base import Input


class XclipPrimaryInput(Input):
    @classmethod
    def name(cls):
        return 'xclip-primary'

    @classmethod
    def is_available(cls):
        return shutil.which('xclip') is not None

    def read(self) -> str:
        try:
            return subprocess.check_output(['xclip',
                                            '-out',
                                            '-selection', 'primary',
                                            '-target', 'UTF8_STRING']).decode('utf-8')
        except UnicodeDecodeError:
            return ''


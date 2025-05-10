from typing import Optional

from clipboard_processor.output._base import Output


class StdoutOutput(Output):

    BOLD = '\033[1m'
    RESET = '\033[0m'

    @classmethod
    def name(cls):
        return 'stdout'

    @classmethod
    def is_available(cls):
        return True

    def show(self, title: str, content: str, timeout: Optional[int] = None):
        print(f'{StdoutOutput.BOLD}{title}{StdoutOutput.RESET}\n{content}')

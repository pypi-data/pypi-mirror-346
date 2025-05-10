from clipboard_processor.input._base import Input

try:
    import pyperclip
except ImportError:
    pyperclip = None


class PyperclipInput(Input):

    @classmethod
    def name(cls):
        return 'auto'

    @classmethod
    def is_available(cls):
        return pyperclip is not None

    def read(self) -> str:
        try:
            return pyperclip.paste()
        except UnicodeDecodeError:
            return ''

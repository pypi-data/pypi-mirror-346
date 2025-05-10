import base64

from clipboard_processor.plugins._base import Plugin

_DECODERS = [
    lambda s: base64.b64decode(s, validate=True).decode('utf-8'),
]


class Base64Plugin(Plugin):

    @classmethod
    def name(cls) -> str:
        return 'base64'

    @classmethod
    def is_available(cls) -> bool:
        return True

    def process(self, data: str) -> list[str]:
        results = []
        for decoder in _DECODERS:
            try:
                results.append(decoder(data))
            except ValueError:
                pass
        return results

    @classmethod
    def example_input(cls) -> str:
        return 'SGVsbG8gV29ybGQh'

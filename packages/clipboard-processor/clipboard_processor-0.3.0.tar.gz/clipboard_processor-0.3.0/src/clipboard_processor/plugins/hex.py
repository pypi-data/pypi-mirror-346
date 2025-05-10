import binascii

from clipboard_processor.plugins._base import Plugin

_DECODERS = [
    lambda s: binascii.a2b_hex(s.encode()).decode('utf-8'),
]


class HexPlugin(Plugin):

    @classmethod
    def name(cls) -> str:
        return 'hex-utf8'

    @classmethod
    def is_available(cls) -> bool:
        return True

    def process(self, data: str) -> list[str]:
        results = []
        for decoder in _DECODERS:
            try:
                decoded = decoder(data)
                if decoded.isprintable():
                    results.append(decoder(data))
            except ValueError:
                pass
        return results

    @classmethod
    def example_input(cls) -> str:
        return '74657374'

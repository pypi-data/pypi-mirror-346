import re

from clipboard_processor.plugins._base import Plugin

try:
    import vininfo
except ImportError:
    vininfo = None


class VinPlugin(Plugin):
    """
    Parse VIN (Vehicle Identification Number) strings to their human-readable representation.
    Requires the vininfo package to be installed.
    """

    def __init__(self):
        super(VinPlugin, self).__init__()
        self._regex = re.compile(r'^[A-HJ-NPR-Z\d]{17}$')

    @classmethod
    def name(cls):
        return 'vin'

    @classmethod
    def is_available(cls):
        return vininfo is not None

    def process(self, data: str) -> list[str]:
        if not self._regex.match(data):
            return []
        info = vininfo.Vin(data)

        result = [k + ': ' + v for k, v in info.annotate().items()]
        if not info.verify_checksum():
            return result + ['Checksum invalid!']
        if info.details:
            for k, v in info.details.annotate().items():
                result.append(k + ': ' + v)
        return result

    @classmethod
    def example_input(cls) -> str:
        return '1HGCM82633A123456'

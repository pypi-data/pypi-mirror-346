from clipboard_processor.plugins._base import Plugin

try:
    import ulid
except ImportError:
    ulid = None


class UlidPlugin(Plugin):
    """
    Parse ULID (Universally Unique Lexicographically Sortable Identifier) strings to their datetime representation.
    Requires the ulid package to be installed.
    """
    @classmethod
    def name(cls) -> str:
        return 'ulid'

    @classmethod
    def is_available(cls) -> bool:
        return ulid is not None

    def process(self, data: str) -> list[str]:
        if len(data) != 26:
            return []
        try:
            u = ulid.ULID.from_str(data)
            return ['ULID at ' + u.datetime.isoformat().replace('+00:00', 'Z').replace('T', ' ')]
        except ValueError:
            return []

    @classmethod
    def example_input(cls) -> str:
        if ulid is None:
            return '01ARZ3NDEKTSV4RRFFQ69G5FAV'
        else:
            return str(ulid.ULID())

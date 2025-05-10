from clipboard_processor.plugins import Plugin


class WellKnownPlugin(Plugin):
    """
    Show explanation for well known "magic" strings.
    """

    STRINGS = {
        '4b825dc642cb6eb9a060e54bf8d69288fbee4904': 'git empty tree object hash (sha1)',
        '6ef19b41225c5369f1c104d45d8d85efa9b057b53b14b4b9b939dd74decc5321': 'git empty tree object hash (sha256)',
    }

    @classmethod
    def name(cls) -> str:
        return 'well-known'

    @classmethod
    def is_available(cls) -> bool:
        return True

    def process(self, data: str) -> list[str]:
        if data in self.STRINGS:
            return [self.STRINGS[data]]
        return []

    @classmethod
    def example_input(cls) -> str:
        return next(iter(cls.STRINGS))

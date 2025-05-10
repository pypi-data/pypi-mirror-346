from clipboard_processor.plugins._base import Plugin

try:
    import cron_descriptor
except ImportError:
    cron_descriptor = None


class CronPlugin(Plugin):
    """
    Parse cron expressions to a human-readable description
    Requires the cron-descriptor package to be installed.
    """

    @classmethod
    def name(cls) -> str:
        return 'cron'

    @classmethod
    def is_available(cls) -> bool:
        return cron_descriptor is not None

    def process(self, data: str) -> list[str]:
        results = []
        try:
            cron = str(cron_descriptor.ExpressionDescriptor(expression=data, use_24hour_time_format=True))
            results.append(cron)
        except cron_descriptor.Exception.FormatException:
            pass
        return results

    @classmethod
    def example_input(cls) -> str:
        return '0 5 ? * MON-FRI *'


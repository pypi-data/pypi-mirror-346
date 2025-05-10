import configparser
import pathlib

from clipboard_processor.plugins._base import Plugin

_CONFIG_FILE = pathlib.Path('~/.aws/config').expanduser()


class AwsAccountIdPlugin(Plugin):
    """
    Parse the 12-digit AWS account ids and resolve the account name using the file ~/.aws/config.
    The name is resolved via the parameters 'sso_account_id' and 'sso_account_name' in the config file.
    Requires the file ~/.aws/config to be present.
    """

    def __init__(self):
        import re
        self._regex = re.compile(r'^\d{12}$')

    @classmethod
    def name(cls) -> str:
        return 'aws-account-id'

    @classmethod
    def is_available(cls):
        return _CONFIG_FILE.exists()

    def process(self, data: str) -> list[str]:
        m = self._regex.match(data)
        if m:
            mapping = _get_aws_account_mapping()
            account_name = mapping.get(m.group(0))
            if account_name:
                return [account_name]
        return []

    @classmethod
    def example_input(cls) -> str:
        return '123456789012'


def _get_aws_account_mapping():
    aws_config = configparser.ConfigParser()
    aws_config.read(_CONFIG_FILE)
    mapping = {}
    for section in aws_config:
        account_id = aws_config.get(section, 'sso_account_id', fallback=None)
        account_name = aws_config.get(section, 'sso_account_name', fallback=None)
        if account_id and account_name:
            mapping[account_id] = account_name
    return mapping

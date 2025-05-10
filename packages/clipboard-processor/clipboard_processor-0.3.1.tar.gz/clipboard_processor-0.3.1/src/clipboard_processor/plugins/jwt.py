import json

from clipboard_processor.plugins._base import Plugin

try:
    import jwt
except ImportError:
    jwt = None


class JwtPlugin(Plugin):
    """
    Decode JWT tokens according to RFC 7519 to the contained JSON object.
    Requires the PyJWT package to be installed.
    """

    def __init__(self):
        super().__init__()

    @classmethod
    def name(cls) -> str:
        return 'jwt'

    @classmethod
    def is_available(cls) -> bool:
        return jwt is not None

    def process(self, data: str) -> list[str]:
        if data.startswith('Bearer '):
            data = data[7:]
        data = self._pad_base64(data)
        try:
            decoded = jwt.decode(data, options={'verify_signature': False})
            return [json.dumps(decoded, indent=2)]
        except jwt.InvalidTokenError:
            return []

    @staticmethod
    def _pad_base64(data):
        segments = data.split('.')
        if len(segments) != 3:
            return data
        missing_padding = len(segments[1]) % 4
        if missing_padding != 0:
            segments[1] += '=' * (4 - missing_padding)
        return '.'.join(segments)

    @classmethod
    def example_input(cls) -> str:
        return ('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2dnZWRJbkFzIjoiYWRtaW4iLCJpYXQiOjE0MjI3Nzk2Mzh9.'
                'gzSraSYS8EXBxLN_oWnFSRgCzcmJmMjLiuyu5CSpyHI=')

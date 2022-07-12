import json
from datetime import datetime
from typing import Optional

from .core import log


class Token:
    """ A class for LINE WORKS authentication token """

    def __init__(self, data: dict):
        self._access_token = data.get('access_token')
        self._refresh_token = data.get('refresh_token')
        self._expires_in = data.get('expires_in')
        self._scope = data.get('scope')

        if self._expires_in is None:
            self._expired_at = None
        else:
            self._expires_in = int(self._expires_in)
            now = datetime.now().timestamp()
            self._expired_at = int(now) + int(self._expires_in)

    @property
    def access_token(self) -> str:
        return self._access_token

    @property
    def refresh_token(self) -> str:
        return self._refresh_token

    @property
    def expires_in(self) -> int:
        return self._expires_in

    @property
    def scope(self) -> str:
        return self._scope

    @property
    def expired_at(self) -> Optional[int]:
        """ An expiration timestamp calculated when this instance is created

        The value is equal to now + expires_in.
        """

        return self._expired_at

    @log(log_args=False, log_return=False)
    def to_dict(self) -> dict:
        return {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'expires_in': self.expires_in,
            'scope': self.scope,
            'expired_at': self.expired_at,
        }

    def __str__(self) -> str:
        return json.dumps(self.to_dict())

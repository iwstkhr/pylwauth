from datetime import datetime

import jwt
import requests

from .core import log, NoneValueError
from .models import Token


class AuthApi:
    """ A class for LINE WORKS Service Account authentication api """

    def __init__(
            self,
            client_id: str,
            client_secret: str,
            service_account_id: str,
            private_key: str,
            timeout=10
    ):
        self._client_id = client_id
        self._client_secret = client_secret
        self._service_account_id = service_account_id
        self._private_key = private_key
        self.timeout = timeout

        if self._client_id is None:
            raise NoneValueError('client_id')
        if self._client_secret is None:
            raise NoneValueError('client_secret')
        if self._service_account_id is None:
            raise NoneValueError('service_account_id')
        if self._private_key is None:
            raise NoneValueError('private_key')

    @property
    def client_id(self) -> str:
        return self._client_id

    @property
    def client_secret(self) -> str:
        return self._client_secret

    @property
    def service_account_id(self) -> str:
        return self._service_account_id

    @property
    def private_key(self) -> str:
        return self._private_key

    @log(log_args=False, log_return=False)
    def get_token(self, scope: str) -> Token:
        """ Get an access token with a refresh token.

        See https://developers.worksmobile.com/jp/reference/authorization-sa

        Args:
            scope (str): Scope

        Returns:
            Token: Access token
        """

        assertion = self.__create_jwt()
        api = 'https://auth.worksmobile.com/oauth2/v2.0/token'
        body = {
            'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
            'assertion': assertion,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': scope,
        }
        response = requests.post(api, body, timeout=self.timeout).json()
        return Token(response)

    @log(log_args=False, log_return=False)
    def refresh_token(self, refresh_token: str) -> Token:
        """ Refresh an access token.

        See https://developers.worksmobile.com/jp/reference/authorization-auth

        Args:
            refresh_token (str): Refresh token

        Returns:
            Token: Access token
        """

        api = 'https://auth.worksmobile.com/oauth2/v2.0/token'
        body = {
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }
        response = requests.post(api, body, timeout=self.timeout).json()
        return Token(response)

    @log(log_args=False, log_return=False)
    def __create_jwt(self, expired_in=60) -> str:
        """ Get a JWT for LINE WORKS Service Account Authentication API.

        See https://developers.worksmobile.com/jp/reference/authorization-sa

        Args:
            expired_in (int): Seconds in which JWT expires

        Returns:
            str: JWT
        """

        iat = int(datetime.now().timestamp())
        payload = {
            'iss': self.client_id,
            'sub': self.service_account_id,
            'iat': iat,
            'exp': iat + expired_in,
        }
        return jwt.encode(payload, self.private_key.replace('\\n', '\n'), 'RS256')

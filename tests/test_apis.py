import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch

from pylwauth import AuthApi


class TestAuthApi:
    @pytest.fixture
    def instance(self) -> AuthApi:
        return AuthApi('client_id', 'client_secret', 'service_account_id', 'private_key', 5)

    def test_client_id(self, instance: AuthApi):
        assert instance.client_id == 'client_id'

    def test_client_secret(self, instance: AuthApi):
        assert instance.client_secret == 'client_secret'

    def test_service_account_id(self, instance: AuthApi):
        assert instance.service_account_id == 'service_account_id'

    def test_private_key(self, instance: AuthApi):
        assert instance.private_key == 'private_key'

    def test_timeout(self, instance: AuthApi):
        assert instance.timeout == 5

    @patch('pylwauth.apis.requests')
    def test_get_token(self, requests: MagicMock, instance: AuthApi):
        instance._AuthApi__create_jwt = MagicMock(return_value='assertion')
        requests.post().json.return_value = {
            'access_token': 'access_token',
            'refresh_token': 'refresh_token',
            'expires_in': 86400,
            'scope': 'bot',
            'token_type': 'Bearer',
        }
        token = instance.get_token('bot')
        assert token.to_dict() == {
            'access_token': 'access_token',
            'refresh_token': 'refresh_token',
            'expires_in': 86400,
            'scope': 'bot',
            'expired_at': token.expired_at,
        }

    @patch('pylwauth.apis.requests')
    def test_refresh_token(self, requests: MagicMock, instance: AuthApi):
        requests.post().json.return_value = {
            'access_token': 'access_token',
            'expires_in': 86400,
            'scope': 'bot',
            'token_type': 'Bearer',
        }
        token = instance.refresh_token('refresh_token')
        assert token.to_dict() == {
            'access_token': 'access_token',
            'refresh_token': None,
            'expires_in': 86400,
            'scope': 'bot',
            'expired_at': token.expired_at,
        }

    @patch('pylwauth.apis.datetime', return_value=MagicMock(wraps=datetime))
    @patch('pylwauth.apis.jwt.encode', return_value='assertion')
    def test___create_jwt(self, encode: MagicMock, dt: MagicMock, instance: AuthApi):
        dt.now().timestamp.return_value = 100
        assert instance._AuthApi__create_jwt(10) == 'assertion'
        encode.assert_called_once_with({
            'iss': instance.client_id,
            'sub': instance.service_account_id,
            'iat': 100,
            'exp': 110,
        }, 'private_key', 'RS256')

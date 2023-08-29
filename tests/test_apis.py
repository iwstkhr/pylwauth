from datetime import datetime

import pytest
from pytest_mock import MockFixture

from pylwauth import AuthApi, apis


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

    def test_get_token(self, mocker: MockFixture, instance: AuthApi):
        mocker.patch.object(instance, '_AuthApi__create_jwt', return_value='assertion')
        mocker.patch('requests.post', return_value=mocker.MagicMock(json=mocker.MagicMock(return_value={
            'access_token': 'access_token',
            'refresh_token': 'refresh_token',
            'expires_in': 86400,
            'scope': 'bot',
            'token_type': 'Bearer',
        })))
        token = instance.get_token('bot')
        assert token.to_dict() == {
            'access_token': 'access_token',
            'refresh_token': 'refresh_token',
            'expires_in': 86400,
            'scope': 'bot',
            'expired_at': token.expired_at,
        }

    def test_refresh_token(self, mocker: MockFixture, instance: AuthApi):
        mocker.patch('requests.post', return_value=mocker.MagicMock(json=mocker.MagicMock(return_value={
            'access_token': 'access_token',
            'expires_in': 86400,
            'scope': 'bot',
            'token_type': 'Bearer',
        })))
        token = instance.refresh_token('refresh_token')
        assert token.to_dict() == {
            'access_token': 'access_token',
            'refresh_token': None,
            'expires_in': 86400,
            'scope': 'bot',
            'expired_at': token.expired_at,
        }

    def test___create_jwt(self, mocker: MockFixture, instance: AuthApi):
        mocker.patch('pylwauth.apis.datetime', return_value=mocker.MagicMock(wraps=datetime))
        mocker.patch.object(apis.datetime.now(), 'timestamp', return_value=100)
        mocker.patch('pylwauth.apis.jwt.encode', return_value='assertion')
        assert instance._AuthApi__create_jwt(10) == 'assertion'
        apis.jwt.encode.assert_called_once_with({
            'iss': instance.client_id,
            'sub': instance.service_account_id,
            'iat': 100,
            'exp': 110,
        }, 'private_key', 'RS256')

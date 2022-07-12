import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch

from pylwauth import Token


class TestToken:
    @pytest.fixture
    @patch('pylwauth.models.datetime', return_value=MagicMock(wraps=datetime))
    def instance(self, dt: MagicMock) -> Token:
        dt.now().timestamp.return_value = 100
        return Token({
            'access_token': 'access_token',
            'refresh_token': 'refresh_token',
            'expires_in': 10,
            'scope': 'bot',
        })

    def test_access_token(self, instance: Token):
        assert instance.access_token == 'access_token'

    def test_refresh_token(self, instance: Token):
        assert instance.refresh_token == 'refresh_token'

    def test_expires_in(self, instance: Token):
        assert instance.expires_in == 10

    def test_scope(self, instance: Token):
        assert instance.scope == 'bot'

    def test_expired_at(self, instance: Token):
        assert instance.expired_at == 110

    def test_to_dict(self, instance: Token):
        assert instance.to_dict() == {
            'access_token': 'access_token',
            'refresh_token': 'refresh_token',
            'expires_in': 10,
            'scope': 'bot',
            'expired_at': 110,
        }

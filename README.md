# pylwauth
An unofficial library for LINE WORKS Service Account Authentication (API 2.0)

https://developers.worksmobile.com/jp/reference/authorization-sa

## Usage
This library cannot be installed through PyPI for now.

```shell
$ pip install git+https://github.com/iwstkhr/pylwauth
```

```python
import json

from pylwauth import AuthApi

CLIENT_ID = 'xxxxxxxxxxxxxxxxxxxx'
CLIENT_SECRET = 'xxxxxxxxxx'
SERVICE_ACCOUNT_ID = 'your-service-account@xxx.yy.zz'
PRIVATE_KEY = '''-----BEGIN PRIVATE KEY-----
YOUR PRIVATE KEY
-----END PRIVATE KEY-----'''

api = AuthApi(CLIENT_ID, CLIENT_SECRET, SERVICE_ACCOUNT_ID, PRIVATE_KEY)

# Get an access token.
token = api.get_token(scope='user.read, orgunit.read, bot')
print(json.dumps(token.to_dict(), indent=2))

# {
#   "access_token": "xxxxxxxxxx",
#   "refresh_token": "xxxxxxxxxx",
#   "expires_in": 86400,
#   "scope": "user.read,orgunit.read,bot",
#   "expired_at": 1657732563
# }

# Refresh the token.
# Note that in service account authentication it may be secure to get another access token
# rather than refresh the existing one, because the refresh token is kept alive in 90 days.
token = api.refresh_token(token.refresh_token)
print(json.dumps(token.to_dict(), indent=2))

# {
#   "access_token": "xxxxxxxxxx",
#   "refresh_token": null,
#   "expires_in": 86400,
#   "scope": "user.read,orgunit.read,bot",
#   "expired_at": 1657733553
# }
```

import pytest
import jwt
from datetime import datetime, timedelta, UTC
from infra.config import vvc_config
from ucs.token.create_token import create_access_token


def test_create_access_token():
    data = {'sub': 'vvc-user'}
    token_returned = create_access_token(data)

    decoded_token = jwt.decode(token_returned, vvc_config.JWT_SECRET, algorithms=[vvc_config.JWT_ALGORITHM])

    assert decoded_token['sub'] == data['sub']

    exp_time = datetime.now(UTC) + timedelta(minutes=vvc_config.JWT_EXPIRY)
    assert decoded_token['exp'] <= exp_time.timestamp()

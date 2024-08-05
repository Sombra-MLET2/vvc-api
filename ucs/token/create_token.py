import logging
from datetime import timedelta, datetime, timezone

import jwt

from infra.config import vvc_config

# Oauth JWT
SECRET_KEY = vvc_config.JWT_SECRET
ALGORITHM = vvc_config.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = vvc_config.JWT_EXPIRY


logger = logging.getLogger(__name__)


def create_access_token(data: dict):
    logger.info(f'Creating access token for {data}')

    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta

    to_encode.update({'exp': expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
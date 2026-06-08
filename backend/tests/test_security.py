from datetime import timedelta

from app.core.security import create_token


def test_create_token_contains_jwt_segments():
    token = create_token("1", "access", timedelta(minutes=5), {"role": "user"})
    assert len(token.split(".")) == 3

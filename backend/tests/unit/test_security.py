import pytest
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token
from app.core.config import settings


class TestPasswordHashing:
    def test_hash_and_verify(self):
        password = "SecurePass123!"
        hashed = hash_password(password)
        assert hashed != password
        assert verify_password(password, hashed)

    def test_verify_wrong_password(self):
        hashed = hash_password("correct")
        assert not verify_password("wrong", hashed)

    def test_hash_is_different_each_time(self):
        pwd = "SamePassword1!"
        assert hash_password(pwd) != hash_password(pwd)

    def test_empty_string(self):
        hashed = hash_password("")
        assert verify_password("", hashed)


class TestJWTToken:
    def test_create_and_decode_access_token(self):
        token = create_access_token({"sub": "1"})
        payload = decode_access_token(token)
        assert payload is not None
        assert payload["sub"] == "1"
        assert payload["type"] == "access"

    def test_decode_expired_token(self):
        from datetime import timedelta
        token = create_access_token({"sub": "1"}, expires_delta=timedelta(seconds=-1))
        payload = decode_access_token(token)
        assert payload is None

    def test_decode_invalid_token(self):
        payload = decode_access_token("invalid.token.here")
        assert payload is None

    def test_token_has_exp_claim(self):
        token = create_access_token({"sub": "42"})
        payload = decode_access_token(token)
        assert "exp" in payload

    def test_token_with_custom_data(self):
        token = create_access_token({"sub": "7", "role": "admin"})
        payload = decode_access_token(token)
        assert payload["role"] == "admin"

    def test_token_algorithm(self):
        token = create_access_token({"sub": "1"})
        from jose import jwt
        header = jwt.get_unverified_header(token)
        assert header["alg"] == settings.jwt_algorithm

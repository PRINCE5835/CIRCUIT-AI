import pytest
from app.core.security import create_access_token
from datetime import timedelta


@pytest.mark.asyncio
async def test_register(client):
    response = await client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "SecurePass123!",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    await client.post(
        "/auth/register",
        json={
            "email": "dup@example.com",
            "username": "user1",
            "password": "SecurePass123!",
        },
    )
    response = await client.post(
        "/auth/register",
        json={
            "email": "dup@example.com",
            "username": "user2",
            "password": "SecurePass123!",
        },
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login(client):
    await client.post(
        "/auth/register",
        json={
            "email": "login@example.com",
            "username": "loginuser",
            "password": "SecurePass123!",
        },
    )
    response = await client.post(
        "/auth/login",
        json={
            "email": "login@example.com",
            "password": "SecurePass123!",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client):
    response = await client.post(
        "/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "wrongpassword",
        },
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_refresh_token(client):
    await client.post(
        "/auth/register",
        json={
            "email": "refresh@example.com",
            "username": "refreshuser",
            "password": "SecurePass123!",
        },
    )
    login_resp = await client.post(
        "/auth/login",
        json={
            "email": "refresh@example.com",
            "password": "SecurePass123!",
        },
    )
    refresh_token = login_resp.json()["refresh_token"]
    response = await client.post(
        "/auth/refresh",
        json={
            "refresh_token": refresh_token,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


@pytest.mark.asyncio
async def test_forgot_password_existing_email(client):
    await client.post(
        "/auth/register",
        json={
            "email": "forgot@example.com",
            "username": "forgotuser",
            "password": "SecurePass123!",
        },
    )

    response = await client.post(
        "/auth/forgot-password",
        json={"email": "forgot@example.com"},
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_forgot_password_nonexistent_email(client):
    response = await client.post(
        "/auth/forgot-password",
        json={"email": "nobody@example.com"},
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_reset_password_invalid_token(client):
    response = await client.post(
        "/auth/reset-password",
        json={
            "token": "invalid-token-here",
            "new_password": "NewSecurePass456!",
        },
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_reset_password_valid_token(client):
    await client.post(
        "/auth/register",
        json={
            "email": "resetpw@example.com",
            "username": "resetpwuser",
            "password": "OldPass123!",
        },
    )

    token = create_access_token(
        {"sub": "1", "purpose": "password_reset"},
        expires_delta=timedelta(hours=1),
    )

    response = await client.post(
        "/auth/reset-password",
        json={"token": token, "new_password": "NewSecurePass456!"},
    )
    assert response.status_code == 204

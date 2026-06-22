import pytest


@pytest.mark.asyncio
async def test_register(client):
    response = await client.post("/auth/register", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "SecurePass123!",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    await client.post("/auth/register", json={
        "email": "dup@example.com",
        "username": "user1",
        "password": "SecurePass123!",
    })
    response = await client.post("/auth/register", json={
        "email": "dup@example.com",
        "username": "user2",
        "password": "SecurePass123!",
    })
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login(client):
    await client.post("/auth/register", json={
        "email": "login@example.com",
        "username": "loginuser",
        "password": "SecurePass123!",
    })
    response = await client.post("/auth/login", json={
        "email": "login@example.com",
        "password": "SecurePass123!",
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client):
    response = await client.post("/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "wrongpassword",
    })
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_refresh_token(client):
    await client.post("/auth/register", json={
        "email": "refresh@example.com",
        "username": "refreshuser",
        "password": "SecurePass123!",
    })
    login_resp = await client.post("/auth/login", json={
        "email": "refresh@example.com",
        "password": "SecurePass123!",
    })
    refresh_token = login_resp.json()["refresh_token"]
    response = await client.post("/auth/refresh", json={
        "refresh_token": refresh_token,
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

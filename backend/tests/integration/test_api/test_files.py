import pytest
import uuid


@pytest.mark.asyncio
async def test_upload_file(client):
    email = f"files_{uuid.uuid4().hex[:8]}@example.com"
    await client.post(
        "/auth/register",
        json={
            "email": email,
            "username": email.split("@")[0],
            "password": "SecurePass123!",
        },
    )
    login = (
        await client.post("/auth/login", json={"email": email, "password": "SecurePass123!"})
    ).json()
    headers = {"Authorization": f"Bearer {login['access_token']}"}

    response = await client.post(
        "/files/upload",
        files={"file": ("test.png", b"fake-image-content", "image/png")},
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert "url" in data
    assert "filename" in data
    assert data["url"].startswith("/uploads/")


@pytest.mark.asyncio
async def test_upload_file_unauthorized(client):
    response = await client.post(
        "/files/upload",
        files={"file": ("test.png", b"fake-image-content", "image/png")},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_upload_file_wrong_extension(client):
    email = f"filesext_{uuid.uuid4().hex[:8]}@example.com"
    await client.post(
        "/auth/register",
        json={
            "email": email,
            "username": email.split("@")[0],
            "password": "SecurePass123!",
        },
    )
    login = (
        await client.post("/auth/login", json={"email": email, "password": "SecurePass123!"})
    ).json()
    headers = {"Authorization": f"Bearer {login['access_token']}"}

    response = await client.post(
        "/files/upload",
        files={"file": ("malware.exe", b"bad-content", "application/octet-stream")},
        headers=headers,
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_upload_file_too_large(client):
    email = f"filesbig_{uuid.uuid4().hex[:8]}@example.com"
    await client.post(
        "/auth/register",
        json={
            "email": email,
            "username": email.split("@")[0],
            "password": "SecurePass123!",
        },
    )
    login = (
        await client.post("/auth/login", json={"email": email, "password": "SecurePass123!"})
    ).json()
    headers = {"Authorization": f"Bearer {login['access_token']}"}

    response = await client.post(
        "/files/upload",
        files={"file": ("huge.png", b"x" * (11 * 1024 * 1024), "image/png")},
        headers=headers,
    )
    assert response.status_code == 400

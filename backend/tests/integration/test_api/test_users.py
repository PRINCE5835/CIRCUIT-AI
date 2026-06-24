import pytest


@pytest.fixture
async def user_headers(client):
    await client.post("/auth/register", json={
        "email": "usr_test@example.com", "username": "usrtest", "password": "SecurePass123!",
    })
    login = (await client.post("/auth/login", json={
        "email": "usr_test@example.com", "password": "SecurePass123!",
    })).json()
    return {"Authorization": f"Bearer {login['access_token']}"}


@pytest.mark.asyncio
async def test_get_profile(client, user_headers):
    response = await client.get("/users/me", headers=user_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "usr_test@example.com"
    assert data["username"] == "usrtest"
    assert "id" in data


@pytest.mark.asyncio
async def test_get_profile_unauthenticated(client):
    response = await client.get("/users/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_update_profile(client, user_headers):
    response = await client.patch("/users/me", json={
        "display_name": "Updated Name",
    }, headers=user_headers)
    assert response.status_code == 200
    assert response.json()["display_name"] == "Updated Name"


@pytest.mark.asyncio
async def test_delete_account(client, user_headers):
    response = await client.delete("/users/me", headers=user_headers)
    assert response.status_code == 204

    # Verify can't login after deactivation
    login = await client.post("/auth/login", json={
        "email": "usr_test@example.com", "password": "SecurePass123!",
    })
    assert login.status_code == 401


@pytest.mark.asyncio
async def test_get_user_by_id(client, user_headers):
    # Get own profile first to get ID
    me = (await client.get("/users/me", headers=user_headers)).json()
    user_id = me["id"]

    response = await client.get(f"/users/{user_id}", headers=user_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "usrtest"


@pytest.mark.asyncio
async def test_get_user_not_found(client, user_headers):
    response = await client.get("/users/99999", headers=user_headers)
    assert response.status_code == 404

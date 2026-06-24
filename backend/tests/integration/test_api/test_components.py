import pytest

pytestmark = pytest.mark.asyncio


async def _auth_headers(client):
    email = "comp_auth@example.com"
    username = "compauth"
    await client.post(
        "/auth/register",
        json={
            "email": email,
            "username": username,
            "password": "SecurePass123!",
        },
    )
    login = (
        await client.post("/auth/login", json={"email": email, "password": "SecurePass123!"})
    ).json()
    return {"Authorization": f"Bearer {login['access_token']}"}


async def test_list_components_empty(client):
    response = await client.get("/components")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["items"] == []


async def test_create_component(client):
    headers = await _auth_headers(client)
    response = await client.post(
        "/components",
        json={"name": "Resistor 10k", "category": "resistor", "manufacturer": "Vishay"},
        headers=headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Resistor 10k"
    assert "id" in data


async def test_get_component(client):
    headers = await _auth_headers(client)
    created = (
        await client.post(
            "/components", json={"name": "LED Red", "category": "led"}, headers=headers
        )
    ).json()
    response = await client.get(f"/components/{created['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "LED Red"


async def test_update_component(client):
    headers = await _auth_headers(client)
    created = (
        await client.post(
            "/components", json={"name": "Capacitor", "category": "capacitor"}, headers=headers
        )
    ).json()
    response = await client.patch(
        f"/components/{created['id']}", json={"manufacturer": "Murata"}, headers=headers
    )
    assert response.status_code == 200
    assert response.json()["manufacturer"] == "Murata"


async def test_delete_component(client):
    headers = await _auth_headers(client)
    created = (
        await client.post(
            "/components", json={"name": "Transistor", "category": "transistor"}, headers=headers
        )
    ).json()
    response = await client.delete(f"/components/{created['id']}", headers=headers)
    assert response.status_code == 204


async def test_search_components(client):
    headers = await _auth_headers(client)
    await client.post(
        "/components", json={"name": "Resistor 100", "category": "resistor"}, headers=headers
    )
    await client.post(
        "/components", json={"name": "Capacitor 100", "category": "capacitor"}, headers=headers
    )
    response = await client.get("/components?q=resistor")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert all("resistor" in item["name"].lower() for item in data["items"])


async def test_filter_components_by_category(client):
    headers = await _auth_headers(client)
    await client.post(
        "/components", json={"name": "Resistor A", "category": "resistor"}, headers=headers
    )
    await client.post("/components", json={"name": "LED Blue", "category": "led"}, headers=headers)
    response = await client.get("/components?category=led")
    assert response.status_code == 200
    data = response.json()
    assert all(item["category"] == "led" for item in data["items"])

import pytest
import uuid


@pytest.mark.asyncio
async def test_create_listing(client):
    email = f"mkt_{uuid.uuid4().hex[:8]}@example.com"
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

    comp = (
        await client.post(
            "/components",
            json={
                "name": "Resistor MKT",
                "category": "resistor",
            },
        )
    ).json()

    response = await client.post(
        "/marketplace",
        json={
            "component_id": comp["id"],
            "title": "10x Resistors 10k",
            "price": 2.50,
            "quantity": 10,
            "condition": "new",
        },
        headers=headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "10x Resistors 10k"
    assert data["price"] == 2.50
    assert "id" in data


@pytest.mark.asyncio
async def test_list_listings(client):
    email = f"mktlist_{uuid.uuid4().hex[:8]}@example.com"
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

    comp = (
        await client.post(
            "/components",
            json={
                "name": "Cap MKT",
                "category": "capacitor",
            },
        )
    ).json()

    await client.post(
        "/marketplace",
        json={
            "component_id": comp["id"],
            "title": "Capacitors 100uF",
            "price": 1.00,
        },
        headers=headers,
    )

    response = await client.get("/marketplace", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data


@pytest.mark.asyncio
async def test_get_listing_public(client):
    email = f"mktget_{uuid.uuid4().hex[:8]}@example.com"
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

    comp = (
        await client.post(
            "/components",
            json={
                "name": "LED MKT",
                "category": "led",
            },
        )
    ).json()

    created = (
        await client.post(
            "/marketplace",
            json={
                "component_id": comp["id"],
                "title": "Red LEDs",
                "price": 3.00,
            },
            headers=headers,
        )
    ).json()

    response = await client.get(f"/marketplace/{created['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Red LEDs"


@pytest.mark.asyncio
async def test_update_listing(client):
    email = f"mktupd_{uuid.uuid4().hex[:8]}@example.com"
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

    comp = (
        await client.post(
            "/components",
            json={
                "name": "Update MKT",
                "category": "resistor",
            },
        )
    ).json()

    created = (
        await client.post(
            "/marketplace",
            json={
                "component_id": comp["id"],
                "title": "Old Listing",
                "price": 5.00,
            },
            headers=headers,
        )
    ).json()

    response = await client.patch(
        f"/marketplace/{created['id']}",
        json={
            "title": "Updated Listing",
            "price": 4.50,
        },
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Listing"
    assert data["price"] == 4.50


@pytest.mark.asyncio
async def test_delete_listing(client):
    email = f"mktdel_{uuid.uuid4().hex[:8]}@example.com"
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

    comp = (
        await client.post(
            "/components",
            json={
                "name": "Delete MKT",
                "category": "resistor",
            },
        )
    ).json()

    created = (
        await client.post(
            "/marketplace",
            json={
                "component_id": comp["id"],
                "title": "Delete Me",
                "price": 1.00,
            },
            headers=headers,
        )
    ).json()

    response = await client.delete(f"/marketplace/{created['id']}", headers=headers)
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_listing_ownership(client):
    email1 = f"own1_{uuid.uuid4().hex[:8]}@example.com"
    email2 = f"own2_{uuid.uuid4().hex[:8]}@example.com"

    for e in [email1, email2]:
        await client.post(
            "/auth/register",
            json={
                "email": e,
                "username": e.split("@")[0],
                "password": "SecurePass123!",
            },
        )

    login1 = (
        await client.post("/auth/login", json={"email": email1, "password": "SecurePass123!"})
    ).json()
    login2 = (
        await client.post("/auth/login", json={"email": email2, "password": "SecurePass123!"})
    ).json()
    headers1 = {"Authorization": f"Bearer {login1['access_token']}"}
    headers2 = {"Authorization": f"Bearer {login2['access_token']}"}

    comp = (
        await client.post(
            "/components",
            json={
                "name": "Owner MKT",
                "category": "resistor",
            },
        )
    ).json()

    created = (
        await client.post(
            "/marketplace",
            json={
                "component_id": comp["id"],
                "title": "Owned Listing",
                "price": 10.00,
            },
            headers=headers1,
        )
    ).json()

    response = await client.patch(
        f"/marketplace/{created['id']}", json={"price": 8.00}, headers=headers2
    )
    assert response.status_code == 404

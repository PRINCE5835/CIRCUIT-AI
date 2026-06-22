import pytest


@pytest.mark.asyncio
async def test_list_components_empty(client):
    response = await client.get("/components")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["items"] == []


@pytest.mark.asyncio
async def test_create_component(client):
    response = await client.post(
        "/components",
        json={
            "name": "Resistor 10k",
            "category": "resistor",
            "manufacturer": "Vishay",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Resistor 10k"
    assert data["category"] == "resistor"
    assert "id" in data


@pytest.mark.asyncio
async def test_get_component(client):
    created = (
        await client.post(
            "/components",
            json={
                "name": "LED Red",
                "category": "led",
            },
        )
    ).json()

    response = await client.get(f"/components/{created['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "LED Red"


@pytest.mark.asyncio
async def test_update_component(client):
    created = (
        await client.post(
            "/components",
            json={
                "name": "Capacitor",
                "category": "capacitor",
            },
        )
    ).json()

    response = await client.patch(
        f"/components/{created['id']}",
        json={
            "manufacturer": "Murata",
        },
    )
    assert response.status_code == 200
    assert response.json()["manufacturer"] == "Murata"


@pytest.mark.asyncio
async def test_delete_component(client):
    created = (
        await client.post(
            "/components",
            json={
                "name": "Transistor",
                "category": "transistor",
            },
        )
    ).json()

    response = await client.delete(f"/components/{created['id']}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_search_components(client):
    await client.post(
        "/components",
        json={
            "name": "Resistor 100",
            "category": "resistor",
        },
    )
    await client.post(
        "/components",
        json={
            "name": "Capacitor 100",
            "category": "capacitor",
        },
    )

    response = await client.get("/components?q=resistor")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert all("resistor" in item["name"].lower() for item in data["items"])


@pytest.mark.asyncio
async def test_filter_components_by_category(client):
    await client.post(
        "/components",
        json={
            "name": "Resistor A",
            "category": "resistor",
        },
    )
    await client.post(
        "/components",
        json={
            "name": "LED Blue",
            "category": "led",
        },
    )

    response = await client.get("/components?category=led")
    assert response.status_code == 200
    data = response.json()
    assert all(item["category"] == "led" for item in data["items"])

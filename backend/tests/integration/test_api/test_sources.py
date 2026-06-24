import pytest
import uuid


@pytest.mark.asyncio
async def test_create_source(client):
    email = f"src_{uuid.uuid4().hex[:8]}@example.com"
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
        "/sources",
        json={
            "title": "Test Source",
            "url": f"https://example.com/{uuid.uuid4().hex}.html",
            "source_type": "wikipedia",
            "priority": 3,
        },
        headers=headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Source"
    assert "id" in data


@pytest.mark.asyncio
async def test_list_sources_empty(client):
    response = await client.get("/sources")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data


@pytest.mark.asyncio
async def test_get_source(client):
    email = f"srcget_{uuid.uuid4().hex[:8]}@example.com"
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

    created = (
        await client.post(
            "/sources",
            json={
                "title": "Get Test",
                "url": f"https://example.com/{uuid.uuid4().hex}.html",
                "source_type": "arduino_docs",
            },
            headers=headers,
        )
    ).json()

    response = await client.get(f"/sources/{created['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Get Test"


@pytest.mark.asyncio
async def test_get_source_not_found(client):
    response = await client.get("/sources/99999999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_sources_by_type(client):
    email = f"srcbytype_{uuid.uuid4().hex[:8]}@example.com"
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

    for i in range(2):
        await client.post(
            "/sources",
            json={
                "title": f"Wiki Source {i}",
                "url": f"https://wiki.example.com/{uuid.uuid4().hex}.html",
                "source_type": "wikipedia",
            },
            headers=headers,
        )

    response = await client.get("/sources?source_type=wikipedia")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 2


@pytest.mark.asyncio
async def test_search_sources(client):
    email = f"srcsearch_{uuid.uuid4().hex[:8]}@example.com"
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

    await client.post(
        "/sources",
        json={
            "title": "Arduino Uno Guide",
            "url": f"https://arduino.example.com/{uuid.uuid4().hex}.html",
            "source_type": "arduino_docs",
        },
        headers=headers,
    )

    response = await client.get("/sources?query=Arduino")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert any("Arduino" in item["title"] for item in data["items"])


@pytest.mark.asyncio
async def test_priority_sources(client):
    email = f"srcprio_{uuid.uuid4().hex[:8]}@example.com"
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

    for i in range(3):
        await client.post(
            "/sources",
            json={
                "title": f"Priority Source {i}",
                "url": f"https://prio.example.com/{uuid.uuid4().hex}.html",
                "source_type": "wikipedia",
                "priority": i + 1,
            },
            headers=headers,
        )

    response = await client.get("/sources/priority?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1


@pytest.mark.asyncio
async def test_update_source(client):
    email = f"srcupd_{uuid.uuid4().hex[:8]}@example.com"
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

    created = (
        await client.post(
            "/sources",
            json={
                "title": "Old Title",
                "url": f"https://update.example.com/{uuid.uuid4().hex}.html",
                "source_type": "sparkfun",
            },
            headers=headers,
        )
    ).json()

    response = await client.patch(
        f"/sources/{created['id']}",
        json={
            "title": "New Title",
            "priority": 1,
        },
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"
    assert response.json()["priority"] == 1


@pytest.mark.asyncio
async def test_delete_source(client):
    email = f"srcdel_{uuid.uuid4().hex[:8]}@example.com"
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

    created = (
        await client.post(
            "/sources",
            json={
                "title": "Delete Me",
                "url": f"https://delete.example.com/{uuid.uuid4().hex}.html",
                "source_type": "other",
            },
            headers=headers,
        )
    ).json()

    response = await client.delete(f"/sources/{created['id']}", headers=headers)
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_create_attribution(client):
    email = f"attrib_{uuid.uuid4().hex[:8]}@example.com"
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

    src = (
        await client.post(
            "/sources",
            json={
                "title": "Attribution Source",
                "url": f"https://attr.example.com/{uuid.uuid4().hex}.html",
                "source_type": "wikipedia",
            },
            headers=headers,
        )
    ).json()

    response = await client.post(
        "/sources/attributions",
        json={
            "source_id": src["id"],
            "content_type": "component",
            "content_id": 42,
            "usage_context": "specification",
            "attribution_text": "Data from Wikipedia",
            "relevance_score": 0.9,
        },
        headers=headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["source_id"] == src["id"]
    assert data["content_type"] == "component"


@pytest.mark.asyncio
async def test_get_content_attributions(client):
    email = f"attribget_{uuid.uuid4().hex[:8]}@example.com"
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

    src = (
        await client.post(
            "/sources",
            json={
                "title": "Content Source",
                "url": f"https://content.example.com/{uuid.uuid4().hex}.html",
                "source_type": "electronics_tutorials",
            },
            headers=headers,
        )
    ).json()

    await client.post(
        "/sources/attributions",
        json={
            "source_id": src["id"],
            "content_type": "circuit",
            "content_id": 99,
        },
        headers=headers,
    )

    response = await client.get("/sources/attributions/circuit/99")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1

import pytest


@pytest.mark.asyncio
async def test_create_conversation(client):
    await client.post(
        "/auth/register",
        json={
            "email": "conv@example.com",
            "username": "convuser",
            "password": "SecurePass123!",
        },
    )
    login = (
        await client.post(
            "/auth/login",
            json={
                "email": "conv@example.com",
                "password": "SecurePass123!",
            },
        )
    ).json()
    token = login["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.post(
        "/conversations",
        json={
            "title": "My Chat",
        },
        headers=headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "My Chat"
    assert "id" in data


@pytest.mark.asyncio
async def test_list_conversations(client):
    await client.post(
        "/auth/register",
        json={
            "email": "listconv@example.com",
            "username": "listconvuser",
            "password": "SecurePass123!",
        },
    )
    login = (
        await client.post(
            "/auth/login",
            json={
                "email": "listconv@example.com",
                "password": "SecurePass123!",
            },
        )
    ).json()
    token = login["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    await client.post("/conversations", json={"title": "Chat 1"}, headers=headers)
    await client.post("/conversations", json={"title": "Chat 2"}, headers=headers)

    response = await client.get("/conversations", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 2
    assert len(data["items"]) >= 2


@pytest.mark.asyncio
async def test_search_conversations(client):
    await client.post(
        "/auth/register",
        json={
            "email": "searchconv@example.com",
            "username": "searchconvuser",
            "password": "SecurePass123!",
        },
    )
    login = (
        await client.post(
            "/auth/login",
            json={
                "email": "searchconv@example.com",
                "password": "SecurePass123!",
            },
        )
    ).json()
    token = login["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    await client.post("/conversations", json={"title": "Arduino Guide"}, headers=headers)
    await client.post("/conversations", json={"title": "Raspberry Pi Setup"}, headers=headers)

    response = await client.get("/conversations?q=arduino", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert any("Arduino" in c["title"] for c in data["items"])


@pytest.mark.asyncio
async def test_get_conversation(client):
    await client.post(
        "/auth/register",
        json={
            "email": "getconv@example.com",
            "username": "getconvuser",
            "password": "SecurePass123!",
        },
    )
    login = (
        await client.post(
            "/auth/login",
            json={
                "email": "getconv@example.com",
                "password": "SecurePass123!",
            },
        )
    ).json()
    token = login["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    created = (
        await client.post("/conversations", json={"title": "Get Me"}, headers=headers)
    ).json()
    response = await client.get(f"/conversations/{created['id']}", headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Get Me"


@pytest.mark.asyncio
async def test_update_conversation_title(client):
    await client.post(
        "/auth/register",
        json={
            "email": "titleconv@example.com",
            "username": "titleconvuser",
            "password": "SecurePass123!",
        },
    )
    login = (
        await client.post(
            "/auth/login",
            json={
                "email": "titleconv@example.com",
                "password": "SecurePass123!",
            },
        )
    ).json()
    token = login["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    created = (
        await client.post("/conversations", json={"title": "Old Title"}, headers=headers)
    ).json()

    response = await client.put(
        f"/conversations/{created['id']}/title",
        json={
            "title": "New Title",
        },
        headers=headers,
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_conversation(client):
    await client.post(
        "/auth/register",
        json={
            "email": "delconv@example.com",
            "username": "delconvuser",
            "password": "SecurePass123!",
        },
    )
    login = (
        await client.post(
            "/auth/login",
            json={
                "email": "delconv@example.com",
                "password": "SecurePass123!",
            },
        )
    ).json()
    token = login["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    created = (
        await client.post("/conversations", json={"title": "Delete Me"}, headers=headers)
    ).json()

    response = await client.delete(f"/conversations/{created['id']}", headers=headers)
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_add_message(client):
    await client.post(
        "/auth/register",
        json={
            "email": "msg@example.com",
            "username": "msguser",
            "password": "SecurePass123!",
        },
    )
    login = (
        await client.post(
            "/auth/login",
            json={
                "email": "msg@example.com",
                "password": "SecurePass123!",
            },
        )
    ).json()
    token = login["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    conv = (await client.post("/conversations", json={"title": "Messages"}, headers=headers)).json()

    response = await client.post(
        f"/conversations/{conv['id']}/messages",
        json={
            "role": "user",
            "content": "Hello!",
        },
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["messages"]) == 1
    assert data["messages"][0]["role"] == "user"
    assert data["messages"][0]["content"] == "Hello!"


@pytest.mark.asyncio
async def test_update_conversation_full(client):
    await client.post(
        "/auth/register",
        json={
            "email": "fullup@example.com",
            "username": "fullupuser",
            "password": "SecurePass123!",
        },
    )
    login = (
        await client.post(
            "/auth/login",
            json={"email": "fullup@example.com", "password": "SecurePass123!"},
        )
    ).json()
    headers = {"Authorization": f"Bearer {login['access_token']}"}

    conv = (
        await client.post(
            "/conversations", json={"title": "Original Title"}, headers=headers
        )
    ).json()

    response = await client.put(
        f"/conversations/{conv['id']}",
        json={
            "title": "Updated Title",
            "messages": [{"role": "user", "content": "Hello"}],
        },
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert len(data["messages"]) >= 1

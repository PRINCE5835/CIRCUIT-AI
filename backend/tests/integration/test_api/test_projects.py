import pytest


@pytest.mark.asyncio
async def test_list_projects_empty(client):
    response = await client.get("/projects")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_project(client):
    await client.post("/auth/register", json={
        "email": "proj@example.com", "username": "projuser", "password": "SecurePass123!",
    })
    login = (await client.post("/auth/login", json={
        "email": "proj@example.com", "password": "SecurePass123!",
    })).json()
    token = login["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.post("/projects", json={
        "title": "My Test Project",
        "description": "A test project",
    }, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "My Test Project"
    assert data["description"] == "A test project"
    assert data["status"] == "draft"
    assert "id" in data


@pytest.mark.asyncio
async def test_list_projects(client):
    await client.post("/auth/register", json={
        "email": "listproj@example.com", "username": "listuser", "password": "SecurePass123!",
    })
    login = (await client.post("/auth/login", json={
        "email": "listproj@example.com", "password": "SecurePass123!",
    })).json()
    token = login["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    await client.post("/projects", json={"title": "Project 1"}, headers=headers)
    await client.post("/projects", json={"title": "Project 2"}, headers=headers)

    response = await client.get("/projects", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2


@pytest.mark.asyncio
async def test_get_project(client):
    await client.post("/auth/register", json={
        "email": "getproj@example.com", "username": "getuser", "password": "SecurePass123!",
    })
    login = (await client.post("/auth/login", json={
        "email": "getproj@example.com", "password": "SecurePass123!",
    })).json()
    token = login["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    created = (await client.post("/projects", json={"title": "Get Me"},
                                  headers=headers)).json()

    response = await client.get(f"/projects/{created['id']}", headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Get Me"


@pytest.mark.asyncio
async def test_update_project(client):
    await client.post("/auth/register", json={
        "email": "updateproj@example.com", "username": "updateuser", "password": "SecurePass123!",
    })
    login = (await client.post("/auth/login", json={
        "email": "updateproj@example.com", "password": "SecurePass123!",
    })).json()
    token = login["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    created = (await client.post("/projects", json={"title": "Original"},
                                  headers=headers)).json()

    response = await client.patch(f"/projects/{created['id']}", json={
        "title": "Updated", "status": "completed",
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"
    assert response.json()["status"] == "completed"


@pytest.mark.asyncio
async def test_delete_project(client):
    await client.post("/auth/register", json={
        "email": "delproj@example.com", "username": "deluser", "password": "SecurePass123!",
    })
    login = (await client.post("/auth/login", json={
        "email": "delproj@example.com", "password": "SecurePass123!",
    })).json()
    token = login["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    created = (await client.post("/projects", json={"title": "Delete Me"},
                                  headers=headers)).json()

    response = await client.delete(f"/projects/{created['id']}", headers=headers)
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_project_ownership(client):
    await client.post("/auth/register", json={
        "email": "owner1@example.com", "username": "owner1", "password": "SecurePass123!",
    })
    await client.post("/auth/register", json={
        "email": "owner2@example.com", "username": "owner2", "password": "SecurePass123!",
    })
    login1 = (await client.post("/auth/login", json={
        "email": "owner1@example.com", "password": "SecurePass123!",
    })).json()
    login2 = (await client.post("/auth/login", json={
        "email": "owner2@example.com", "password": "SecurePass123!",
    })).json()

    created = (await client.post("/projects", json={"title": "Owner1 Project"},
                                  headers={"Authorization": f"Bearer {login1['access_token']}"})).json()

    response = await client.get(f"/projects/{created['id']}",
                                headers={"Authorization": f"Bearer {login2['access_token']}"})
    assert response.status_code == 404

import pytest


@pytest.mark.asyncio
async def test_create_circuit(client):
    await client.post("/auth/register", json={
        "email": "circ@example.com", "username": "circuser", "password": "SecurePass123!",
    })
    login = (await client.post("/auth/login", json={
        "email": "circ@example.com", "password": "SecurePass123!",
    })).json()
    token = login["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    proj = (await client.post("/projects", json={"title": "Circuit Proj"}, headers=headers)).json()

    response = await client.post("/circuits", json={
        "name": "Test Circuit",
        "project_id": proj["id"],
        "circuit_data": {"type": "blinker", "components": ["R1", "LED1"]},
    }, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Circuit"
    assert data["circuit_data"] == {"type": "blinker", "components": ["R1", "LED1"]}
    assert "id" in data
    assert data["project_id"] == proj["id"]


@pytest.mark.asyncio
async def test_list_circuits(client):
    await client.post("/auth/register", json={
        "email": "circ_list@example.com", "username": "circ_list", "password": "SecurePass123!",
    })
    login = (await client.post("/auth/login", json={
        "email": "circ_list@example.com", "password": "SecurePass123!",
    })).json()
    token = login["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    proj = (await client.post("/projects", json={"title": "List Proj"}, headers=headers)).json()

    await client.post("/circuits", json={
        "name": "C1", "project_id": proj["id"], "circuit_data": {},
    }, headers=headers)
    await client.post("/circuits", json={
        "name": "C2", "project_id": proj["id"], "circuit_data": {},
    }, headers=headers)

    response = await client.get("/circuits", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 2


@pytest.mark.asyncio
async def test_get_circuit(client):
    await client.post("/auth/register", json={
        "email": "circ_get@example.com", "username": "circ_get", "password": "SecurePass123!",
    })
    login = (await client.post("/auth/login", json={
        "email": "circ_get@example.com", "password": "SecurePass123!",
    })).json()
    token = login["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    proj = (await client.post("/projects", json={"title": "Get Proj"}, headers=headers)).json()

    created = (await client.post("/circuits", json={
        "name": "Get Me", "project_id": proj["id"], "circuit_data": {"key": "val"},
    }, headers=headers)).json()

    response = await client.get(f"/circuits/{created['id']}", headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Get Me"


@pytest.mark.asyncio
async def test_get_circuit_not_found(client):
    await client.post("/auth/register", json={
        "email": "circ_nf@example.com", "username": "circ_nf", "password": "SecurePass123!",
    })
    login = (await client.post("/auth/login", json={
        "email": "circ_nf@example.com", "password": "SecurePass123!",
    })).json()
    token = login["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.get("/circuits/99999", headers=headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_circuit(client):
    await client.post("/auth/register", json={
        "email": "circ_upd@example.com", "username": "circ_upd", "password": "SecurePass123!",
    })
    login = (await client.post("/auth/login", json={
        "email": "circ_upd@example.com", "password": "SecurePass123!",
    })).json()
    token = login["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    proj = (await client.post("/projects", json={"title": "Upd Proj"}, headers=headers)).json()

    created = (await client.post("/circuits", json={
        "name": "Original", "project_id": proj["id"], "circuit_data": {},
    }, headers=headers)).json()

    response = await client.patch(f"/circuits/{created['id']}", json={
        "name": "Updated",
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated"


@pytest.mark.asyncio
async def test_delete_circuit(client):
    await client.post("/auth/register", json={
        "email": "circ_del@example.com", "username": "circ_del", "password": "SecurePass123!",
    })
    login = (await client.post("/auth/login", json={
        "email": "circ_del@example.com", "password": "SecurePass123!",
    })).json()
    token = login["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    proj = (await client.post("/projects", json={"title": "Del Proj"}, headers=headers)).json()

    created = (await client.post("/circuits", json={
        "name": "Delete Me", "project_id": proj["id"], "circuit_data": {},
    }, headers=headers)).json()

    response = await client.delete(f"/circuits/{created['id']}", headers=headers)
    assert response.status_code == 204

    # Verify gone
    get_resp = await client.get(f"/circuits/{created['id']}", headers=headers)
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_circuit_ownership(client):
    await client.post("/auth/register", json={
        "email": "circ_own1@example.com", "username": "circ_own1", "password": "SecurePass123!",
    })
    await client.post("/auth/register", json={
        "email": "circ_own2@example.com", "username": "circ_own2", "password": "SecurePass123!",
    })
    login1 = (await client.post("/auth/login", json={
        "email": "circ_own1@example.com", "password": "SecurePass123!",
    })).json()
    login2 = (await client.post("/auth/login", json={
        "email": "circ_own2@example.com", "password": "SecurePass123!",
    })).json()

    h1 = {"Authorization": f"Bearer {login1['access_token']}"}
    h2 = {"Authorization": f"Bearer {login2['access_token']}"}

    proj = (await client.post("/projects", json={"title": "Own Proj"}, headers=h1)).json()
    created = (await client.post("/circuits", json={
        "name": "Owned", "project_id": proj["id"], "circuit_data": {},
    }, headers=h1)).json()

    # User2 should not see user1's circuit
    response = await client.get(f"/circuits/{created['id']}", headers=h2)
    assert response.status_code == 404

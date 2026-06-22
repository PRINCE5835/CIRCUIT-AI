import pytest


@pytest.mark.asyncio
async def test_create_safety_report(client):
    # Need a circuit first
    register = await client.post("/auth/register", json={
        "email": "safety_reg@example.com", "username": "safety_reg", "password": "SecurePass123!",
    })
    login = (await client.post("/auth/login", json={
        "email": "safety_reg@example.com", "password": "SecurePass123!",
    })).json()
    token = login["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    proj = (await client.post("/projects", json={"title": "Safety Project"}, headers=headers)).json()
    circuit = (await client.post("/circuits", json={
        "name": "Test Circuit",
        "project_id": proj["id"],
        "circuit_data": {"type": "simple"},
    }, headers=headers)).json()

    response = await client.post("/safety-reports", json={
        "circuit_id": circuit["id"],
        "severity": "medium",
        "recommendations": "Check voltage ratings",
    }, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "pending"
    assert data["severity"] == "medium"
    assert "id" in data


@pytest.mark.asyncio
async def test_list_safety_reports(client):
    register = await client.post("/auth/register", json={
        "email": "safety_list@example.com", "username": "safety_list", "password": "SecurePass123!",
    })
    login = (await client.post("/auth/login", json={
        "email": "safety_list@example.com", "password": "SecurePass123!",
    })).json()
    token = login["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    proj = (await client.post("/projects", json={"title": "For Listing"}, headers=headers)).json()
    circuit = (await client.post("/circuits", json={
        "name": "List Circuit", "project_id": proj["id"], "circuit_data": {},
    }, headers=headers)).json()

    await client.post("/safety-reports", json={
        "circuit_id": circuit["id"], "severity": "low",
    }, headers=headers)
    await client.post("/safety-reports", json={
        "circuit_id": circuit["id"], "severity": "high",
    }, headers=headers)

    response = await client.get("/safety-reports", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 2


@pytest.mark.asyncio
async def test_get_safety_report(client):
    register = await client.post("/auth/register", json={
        "email": "safety_get@example.com", "username": "safety_get", "password": "SecurePass123!",
    })
    login = (await client.post("/auth/login", json={
        "email": "safety_get@example.com", "password": "SecurePass123!",
    })).json()
    token = login["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    proj = (await client.post("/projects", json={"title": "Get Proj"}, headers=headers)).json()
    circuit = (await client.post("/circuits", json={
        "name": "Get Circuit", "project_id": proj["id"], "circuit_data": {},
    }, headers=headers)).json()
    created = (await client.post("/safety-reports", json={
        "circuit_id": circuit["id"], "severity": "high",
    }, headers=headers)).json()

    response = await client.get(f"/safety-reports/{created['id']}", headers=headers)
    assert response.status_code == 200
    assert response.json()["severity"] == "high"


@pytest.mark.asyncio
async def test_update_safety_report(client):
    register = await client.post("/auth/register", json={
        "email": "safety_upd@example.com", "username": "safety_upd", "password": "SecurePass123!",
    })
    login = (await client.post("/auth/login", json={
        "email": "safety_upd@example.com", "password": "SecurePass123!",
    })).json()
    token = login["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    proj = (await client.post("/projects", json={"title": "Upd Proj"}, headers=headers)).json()
    circuit = (await client.post("/circuits", json={
        "name": "Upd Circuit", "project_id": proj["id"], "circuit_data": {},
    }, headers=headers)).json()
    created = (await client.post("/safety-reports", json={
        "circuit_id": circuit["id"], "severity": "low",
    }, headers=headers)).json()

    response = await client.patch(f"/safety-reports/{created['id']}", json={
        "severity": "high", "status": "reviewed",
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["severity"] == "high"
    assert response.json()["status"] == "reviewed"


@pytest.mark.asyncio
async def test_delete_safety_report(client):
    register = await client.post("/auth/register", json={
        "email": "safety_del@example.com", "username": "safety_del", "password": "SecurePass123!",
    })
    login = (await client.post("/auth/login", json={
        "email": "safety_del@example.com", "password": "SecurePass123!",
    })).json()
    token = login["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    proj = (await client.post("/projects", json={"title": "Del Proj"}, headers=headers)).json()
    circuit = (await client.post("/circuits", json={
        "name": "Del Circuit", "project_id": proj["id"], "circuit_data": {},
    }, headers=headers)).json()
    created = (await client.post("/safety-reports", json={
        "circuit_id": circuit["id"], "severity": "low",
    }, headers=headers)).json()

    response = await client.delete(f"/safety-reports/{created['id']}", headers=headers)
    assert response.status_code == 204

import pytest


@pytest.mark.asyncio
async def test_create_cost_estimate(client):
    await client.post(
        "/auth/register",
        json={
            "email": "cost_reg@example.com",
            "username": "cost_reg",
            "password": "SecurePass123!",
        },
    )
    login = (
        await client.post(
            "/auth/login",
            json={
                "email": "cost_reg@example.com",
                "password": "SecurePass123!",
            },
        )
    ).json()
    token = login["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    proj = (await client.post("/projects", json={"title": "Cost Project"}, headers=headers)).json()

    response = await client.post(
        "/cost-estimates",
        json={
            "project_id": proj["id"],
            "total_cost": 45.50,
            "currency": "USD",
        },
        headers=headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["total_cost"] == 45.50
    assert data["currency"] == "USD"
    assert "id" in data


@pytest.mark.asyncio
async def test_list_cost_estimates(client):
    await client.post(
        "/auth/register",
        json={
            "email": "cost_list@example.com",
            "username": "cost_list",
            "password": "SecurePass123!",
        },
    )
    login = (
        await client.post(
            "/auth/login",
            json={
                "email": "cost_list@example.com",
                "password": "SecurePass123!",
            },
        )
    ).json()
    token = login["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    proj = (
        await client.post("/projects", json={"title": "List Cost Proj"}, headers=headers)
    ).json()
    await client.post(
        "/cost-estimates",
        json={
            "project_id": proj["id"],
            "total_cost": 10.0,
            "currency": "USD",
        },
        headers=headers,
    )
    await client.post(
        "/cost-estimates",
        json={
            "project_id": proj["id"],
            "total_cost": 20.0,
            "currency": "EUR",
        },
        headers=headers,
    )

    response = await client.get("/cost-estimates", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2


@pytest.mark.asyncio
async def test_get_cost_estimate(client):
    await client.post(
        "/auth/register",
        json={
            "email": "cost_get@example.com",
            "username": "cost_get",
            "password": "SecurePass123!",
        },
    )
    login = (
        await client.post(
            "/auth/login",
            json={
                "email": "cost_get@example.com",
                "password": "SecurePass123!",
            },
        )
    ).json()
    token = login["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    proj = (await client.post("/projects", json={"title": "Get Cost Proj"}, headers=headers)).json()
    created = (
        await client.post(
            "/cost-estimates",
            json={
                "project_id": proj["id"],
                "total_cost": 15.0,
                "currency": "USD",
            },
            headers=headers,
        )
    ).json()

    response = await client.get(f"/cost-estimates/{created['id']}", headers=headers)
    assert response.status_code == 200
    assert response.json()["total_cost"] == 15.0


@pytest.mark.asyncio
async def test_delete_cost_estimate(client):
    await client.post(
        "/auth/register",
        json={
            "email": "cost_del@example.com",
            "username": "cost_del",
            "password": "SecurePass123!",
        },
    )
    login = (
        await client.post(
            "/auth/login",
            json={
                "email": "cost_del@example.com",
                "password": "SecurePass123!",
            },
        )
    ).json()
    token = login["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    proj = (await client.post("/projects", json={"title": "Del Cost Proj"}, headers=headers)).json()
    created = (
        await client.post(
            "/cost-estimates",
            json={
                "project_id": proj["id"],
                "total_cost": 5.0,
                "currency": "USD",
            },
            headers=headers,
        )
    ).json()

    response = await client.delete(f"/cost-estimates/{created['id']}", headers=headers)
    assert response.status_code == 204

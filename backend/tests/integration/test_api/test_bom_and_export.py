import pytest


@pytest.mark.asyncio
async def test_add_bom_item(client):
    # Need a user + project + component first
    await client.post(
        "/auth/register",
        json={
            "email": "bom@example.com",
            "username": "bomuser",
            "password": "SecurePass123!",
        },
    )
    login = (
        await client.post(
            "/auth/login",
            json={
                "email": "bom@example.com",
                "password": "SecurePass123!",
            },
        )
    ).json()
    token = login["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    proj = (await client.post("/projects", json={"title": "BOM Project"}, headers=headers)).json()
    comp = (
        await client.post(
            "/components",
            json={
                "name": "Resistor BOM",
                "category": "resistor",
            },
        )
    ).json()

    response = await client.post(
        f"/projects/{proj['id']}/bom",
        json={
            "component_id": comp["id"],
            "quantity": 5,
            "notes": "For LED circuit",
        },
        headers=headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["quantity"] == 5
    assert data["notes"] == "For LED circuit"
    assert data["component_id"] == comp["id"]


@pytest.mark.asyncio
async def test_list_bom(client):
    await client.post(
        "/auth/register",
        json={
            "email": "bomlist@example.com",
            "username": "bomlistuser",
            "password": "SecurePass123!",
        },
    )
    login = (
        await client.post(
            "/auth/login",
            json={
                "email": "bomlist@example.com",
                "password": "SecurePass123!",
            },
        )
    ).json()
    token = login["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    proj = (await client.post("/projects", json={"title": "BOM List Proj"}, headers=headers)).json()
    c1 = (await client.post("/components", json={"name": "C1", "category": "resistor"})).json()
    c2 = (await client.post("/components", json={"name": "C2", "category": "capacitor"})).json()

    await client.post(
        f"/projects/{proj['id']}/bom",
        json={"component_id": c1["id"], "quantity": 2},
        headers=headers,
    )
    await client.post(
        f"/projects/{proj['id']}/bom",
        json={"component_id": c2["id"], "quantity": 3},
        headers=headers,
    )

    response = await client.get(f"/projects/{proj['id']}/bom", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2


@pytest.mark.asyncio
async def test_delete_bom_item(client):
    await client.post(
        "/auth/register",
        json={
            "email": "bomdel@example.com",
            "username": "bomdeluser",
            "password": "SecurePass123!",
        },
    )
    login = (
        await client.post(
            "/auth/login",
            json={
                "email": "bomdel@example.com",
                "password": "SecurePass123!",
            },
        )
    ).json()
    token = login["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    proj = (await client.post("/projects", json={"title": "BOM Del Proj"}, headers=headers)).json()
    comp = (
        await client.post("/components", json={"name": "Delete Me", "category": "resistor"})
    ).json()
    item = (
        await client.post(
            f"/projects/{proj['id']}/bom",
            json={"component_id": comp["id"], "quantity": 1},
            headers=headers,
        )
    ).json()

    response = await client.delete(f"/projects/{proj['id']}/bom/{item['id']}", headers=headers)
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_export_project(client):
    await client.post(
        "/auth/register",
        json={
            "email": "export@example.com",
            "username": "exportuser",
            "password": "SecurePass123!",
        },
    )
    login = (
        await client.post(
            "/auth/login",
            json={
                "email": "export@example.com",
                "password": "SecurePass123!",
            },
        )
    ).json()
    token = login["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    proj = (await client.post("/projects", json={"title": "Export Me"}, headers=headers)).json()
    comp = (
        await client.post("/components", json={"name": "Exp Comp", "category": "resistor"})
    ).json()
    await client.post(
        f"/projects/{proj['id']}/bom",
        json={"component_id": comp["id"], "quantity": 4},
        headers=headers,
    )

    response = await client.get(f"/projects/{proj['id']}/export?fmt=json", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Export Me"
    assert "bom" in data

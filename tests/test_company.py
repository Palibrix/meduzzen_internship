import pytest

from tests.test_user import test_login, test_login_second


@pytest.mark.asyncio
async def test_get_users(test_client):
    token = await test_login(test_client)
    response = await test_client.get("/companies/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_company_not_logged(test_client):
    response = await test_client.post("/companies/create", json={
        "company_name": "string_new",
        "company_title": "string",
        "company_description": "string",
    })
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_company(test_client):
    token = await test_login(test_client)
    response = await test_client.post("/companies/create", headers={"Authorization": f"Bearer {token}"}, json={
        "company_name": "New company",
        "company_title": "string",
        "company_description": "string",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["company_name"] == "New company"


@pytest.mark.asyncio
async def test_update_company(test_client):
    token = await test_login(test_client)
    response = await test_client.put("/companies/1", headers={"Authorization": f"Bearer {token}"}, json={
        "company_name": "New name",
        "company_title": "string",
        "company_description": "string",
        "is_visible": False
    })
    assert response.status_code == 200
    data = response.json()
    assert data["company_name"] == "New name"
    assert data["company_title"] == "string"


@pytest.mark.asyncio
async def test_get_hidden_company_wrong_user(test_client):
    token = await test_login_second(test_client)
    response = await test_client.get("/companies/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_one_company(test_client):
    token = await test_login(test_client)
    response = await test_client.get("/companies/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["company_id"] == 1
    assert data["company_name"] == "New name"


@pytest.mark.asyncio
async def test_delete_company_wrong_user(test_client):
    token = await test_login_second(test_client)
    response = await test_client.delete("/companies/1", headers={"Authorization": f"Bearer {token}"},)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_company(test_client):
    token = await test_login(test_client)
    response = await test_client.delete("/companies/1", headers={"Authorization": f"Bearer {token}"},)
    assert response.status_code == 200

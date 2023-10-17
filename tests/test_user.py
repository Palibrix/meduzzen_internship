import pytest


@pytest.mark.asyncio
async def test_login(test_client):
    response = await test_client.post("/token", data={"username": "test@test.com", "password": "testpassword"})
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token is not None
    return token

@pytest.mark.asyncio
async def test_get_users(test_client):
    response = await test_client.get("/users/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_user(test_client):
    response = await test_client.post("/sign-up/", json={
        "user_email": "test_two@test.com",
        "hashed_password": "testpassword",
        "user_firstname": "Test",
        "user_lastname": "User",
        "user_city": "User",
        "user_phone": "+44 7911 123456",
        "user_avatar": "User",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["user_email"] == "test_two@test.com"
    assert data["user_firstname"] == "Test"
    assert data["user_lastname"] == "User"


@pytest.mark.asyncio
async def test_get_one_user(test_client):
    response = await test_client.get("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 1
    assert data["user_email"] == "test@test.com"
    assert data["user_firstname"] == "Test"
    assert data["user_lastname"] == "User"


@pytest.mark.asyncio
async def test_get_non_existing_user(test_client):
    response = await test_client.get("/users/10")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_user(test_client):
    token = await test_login(test_client)
    response = await test_client.put("/users/1", headers={"Authorization": f"Bearer {token}"}, json={
          "user_firstname": "Updated",
          "user_lastname": "User",
          "user_city": "User",
          "user_phone": "User",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["user_firstname"] == "Updated"
    assert data["user_lastname"] == "User"


@pytest.mark.asyncio
async def test_delete_wrong_user(test_client):
    token = await test_login(test_client)
    response = await test_client.delete("/users/2", headers={"Authorization": f"Bearer {token}"},)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_user(test_client):
    token = await test_login(test_client)
    response = await test_client.delete("/users/1", headers={"Authorization": f"Bearer {token}"},)
    assert response.status_code == 200


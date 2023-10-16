import pytest

from tests.test_user import test_login, test_login_second


@pytest.mark.asyncio
async def test_send_invitation(test_client):
	token = await test_login(test_client)
	response = await test_client.post("/companies/1/invitations?user_id=2",
									headers={"Authorization": f"Bearer {token}"})
	assert response.status_code == 200


@pytest.mark.asyncio
async def test_send_request(test_client):
	token = await test_login_second(test_client)
	response = await test_client.post("/companies/1/requests", headers={"Authorization": f"Bearer {token}"})
	assert response.status_code == 200


@pytest.mark.asyncio
async def test_accept_invitation(test_client):
	token = await test_login_second(test_client)
	response = await test_client.post("/invitations/1/accept", headers={"Authorization": f"Bearer {token}"})
	assert response.status_code == 200


@pytest.mark.asyncio
async def test_cancel_request(test_client):
	token = await test_login_second(test_client)
	response = await test_client.delete("/request/2", headers={"Authorization": f"Bearer {token}"})
	assert response.status_code == 200


@pytest.mark.asyncio
async def test_leave_company(test_client):
	token = await test_login_second(test_client)
	response = await test_client.delete("/companies/1/leave", headers={"Authorization": f"Bearer {token}"})
	assert response.status_code == 200


@pytest.mark.asyncio
async def test_view_requests(test_client):
	token = await test_login(test_client)
	response = await test_client.get("/user/requests", headers={"Authorization": f"Bearer {token}"})
	assert response.status_code == 200


@pytest.mark.asyncio
async def test_view_invitations(test_client):
	token = await test_login(test_client)
	response = await test_client.get("/user/invitations", headers={"Authorization": f"Bearer {token}"})
	assert response.status_code == 200


@pytest.mark.asyncio
async def test_view_invited_users(test_client):
	token = await test_login(test_client)
	response = await test_client.get("/companies/1/invitations", headers={"Authorization": f"Bearer {token}"})
	assert response.status_code == 200


@pytest.mark.asyncio
async def test_view_join_requests(test_client):
	token = await test_login(test_client)
	response = await test_client.get("/companies/1/requests", headers={"Authorization": f"Bearer {token}"})
	assert response.status_code == 200


@pytest.mark.asyncio
async def test_view_company_users(test_client):
	token = await test_login(test_client)
	response = await test_client.get("/companies/1/users", headers={"Authorization": f"Bearer {token}"})
	assert response.status_code == 200

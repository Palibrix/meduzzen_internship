import pytest


@pytest.mark.asyncio
async def test_read_main(test_client):
	response = await test_client.get("/")
	assert response.status_code == 200
	assert response.json() == {
		"status_code": 200,
		"detail": "ok",
		"result": "working"
	}


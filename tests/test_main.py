from fastapi.testclient import TestClient


def test_read_main(test_client: TestClient) -> None:
	response = test_client.get("/")
	assert response.status_code == 200
	assert response.json() == {
		"status_code": 200,
		"detail": "ok",
		"result": "working"
	}

from fastapi.testclient import TestClient

from contactlookup.controller import app

test_api_client = TestClient(app)


def test_read_root():
    response = test_api_client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to the Contact Lookup App. Use the /docs endpoint to see the API documentation.",
    }


# TODO: Add more tests for the remaining endpoints

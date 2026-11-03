from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import contactlookup.controller as app_controller
from contactlookup.controller import app
from contactlookup.definitions import (
    API_KEY_ENV_VAR,
    API_KEY_HEADER,
    ROOT_DIR,
    SAMPLE_CONTACTS_DIR,
    SAMPLE_CONTACTS_FILE,
)
from contactlookup.services.file_data_store_service import FileDataStoreService
from contactlookup.utils import split_unix_path_string

test_api_client = TestClient(app)


@pytest.fixture
def loaded_service(monkeypatch):
    sample_dir = Path("/".join(split_unix_path_string(SAMPLE_CONTACTS_DIR)))
    service = FileDataStoreService()
    service.set_contacts_file_path(ROOT_DIR.parent / sample_dir / SAMPLE_CONTACTS_FILE)
    assert service.initialize()
    monkeypatch.setattr(app_controller, "service", service)
    monkeypatch.delenv(API_KEY_ENV_VAR, raising=False)
    return service


@pytest.fixture
def no_service(monkeypatch):
    monkeypatch.setattr(app_controller, "service", None)
    monkeypatch.delenv(API_KEY_ENV_VAR, raising=False)


def test_read_root():
    response = test_api_client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to the Contact Lookup App. Use the /docs endpoint to see the API documentation.",
    }


def test_health_ok(loaded_service):
    response = test_api_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_without_service(no_service):
    assert test_api_client.get("/health").status_code == 503


def test_contacts_without_service(no_service):
    assert test_api_client.get("/contacts").status_code == 503


def test_read_contacts(loaded_service):
    response = test_api_client.get("/contacts")
    assert response.status_code == 200
    assert len(response.json()["contacts"]) == len(loaded_service.get_contacts())


def test_read_contact(loaded_service):
    response = test_api_client.get("/contacts/1")
    assert response.status_code == 200
    assert response.json()["contact"]["id"] == 1


def test_read_contact_not_found(loaded_service):
    assert test_api_client.get("/contacts/999999").status_code == 404


def test_search_with_no_matches_is_empty_list(loaded_service):
    response = test_api_client.get("/contacts/fname/nobody-has-this-name")
    assert response.status_code == 200
    assert response.json() == {"contacts": []}


def test_api_key_not_required_when_unset(loaded_service):
    assert test_api_client.get("/contacts/1").status_code == 200


def test_api_key_missing(loaded_service, monkeypatch):
    monkeypatch.setenv(API_KEY_ENV_VAR, "s3cret")
    assert test_api_client.get("/contacts/1").status_code == 401


def test_api_key_wrong(loaded_service, monkeypatch):
    monkeypatch.setenv(API_KEY_ENV_VAR, "s3cret")
    response = test_api_client.get("/contacts/1", headers={API_KEY_HEADER: "nope"})
    assert response.status_code == 401


def test_api_key_correct(loaded_service, monkeypatch):
    monkeypatch.setenv(API_KEY_ENV_VAR, "s3cret")
    response = test_api_client.get("/contacts/1", headers={API_KEY_HEADER: "s3cret"})
    assert response.status_code == 200


def test_api_key_does_not_cover_root_and_health(loaded_service, monkeypatch):
    monkeypatch.setenv(API_KEY_ENV_VAR, "s3cret")
    assert test_api_client.get("/").status_code == 200
    assert test_api_client.get("/health").status_code == 200

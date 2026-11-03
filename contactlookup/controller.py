"""Controller for the contactlookup app."""

import os
import secrets

from fastapi import APIRouter, FastAPI, HTTPException, Security, status
from fastapi.security import APIKeyHeader

from contactlookup.definitions import API_KEY_ENV_VAR, API_KEY_HEADER
from contactlookup.services.data_store_service import DataStoreService

app = FastAPI()
service: DataStoreService | None = None

api_key_header = APIKeyHeader(name=API_KEY_HEADER, auto_error=False)


def set_data_store_service(data_store_service: DataStoreService):
    """Set the data store service.

    In the future, we will implement a database service to store contacts. This
    function will be used to set the database service to be used by the
    controller.

    Args:
        data_store_service (DataStoreService): The data store service.
    """
    global service
    service = data_store_service


def require_api_key(api_key: str | None = Security(api_key_header)):
    """Check the X-API-Key header against CONTACTLOOKUP_API_KEY.

    If CONTACTLOOKUP_API_KEY is not set, the API is open to anyone who can
    reach it.
    """
    expected = os.environ.get(API_KEY_ENV_VAR)
    if not expected:
        return
    if not api_key or not secrets.compare_digest(api_key.encode(), expected.encode()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )


def get_service() -> DataStoreService:
    """Return the data store service, or fail with 503 if it isn't set yet."""
    if not service:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Data store service not set",
        )
    return service


@app.get("/")
def read_root():
    """Welcome message."""
    msg = "Welcome to the Contact Lookup App. Use the /docs endpoint to see the API documentation."
    return {"message": msg}


@app.get("/health")
def health():
    """Health check. Returns 503 until the contacts are loaded."""
    get_service()
    return {"status": "ok"}


contacts_router = APIRouter(
    prefix="/contacts",
    dependencies=[Security(require_api_key)],
)


@contacts_router.get("")
def read_contacts():
    """Get all contacts."""
    return {"contacts": get_service().get_contacts()}


@contacts_router.get("/{contact_id}")
def read_contact(contact_id: int):
    """Get contact by ID."""
    contact = get_service().get_contact(contact_id)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No contact with id {contact_id}",
        )
    return {"contact": contact}


@contacts_router.get("/fname/{fname}")
def read_contacts_by_fname(fname: str):
    """Get contacts by first name."""
    return {"contacts": get_service().get_contacts_by_fname(fname)}


@contacts_router.get("/phone/{phone_number}")
def read_contacts_by_phone_number(phone_number: str):
    """Get contacts by phone number."""
    return {"contacts": get_service().get_contacts_by_phone_number(phone_number)}


@contacts_router.get("/email/{email}")
def read_contacts_by_email(email: str):
    """Get contacts by email."""
    return {"contacts": get_service().get_contacts_by_email(email)}


@contacts_router.get("/country/{country}")
def read_contacts_by_country(country: str):
    """Get contacts by country."""
    return {"contacts": get_service().get_contacts_by_country(country)}


@contacts_router.get("/state/{state}")
def read_contacts_by_state(state: str):
    """Get contacts by state."""
    return {"contacts": get_service().get_contacts_by_state(state)}


app.include_router(contacts_router)

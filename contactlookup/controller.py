"""Controller for the contactlookup app."""

from fastapi import FastAPI

from contactlookup.services.data_store_service import DataStoreService

app = FastAPI()
service: DataStoreService | None = None


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


@app.get("/")
def read_root():
    """Welcome message."""
    msg = "Welcome to the Contact Lookup App. Use the /docs endpoint to see the API documentation."
    return {"message": msg}


@app.get("/contacts")
def read_contacts():
    """Get all contacts."""
    if not service:
        return {"Error": "Data store service not set"}
    contacts = service.get_contacts()
    return {"contacts": contacts}


@app.get("/contacts/{contact_id}")
def read_contact(contact_id: int):
    """Get contact by ID."""
    if not service:
        return {"Error": "Data store service not set"}
    contact = service.get_contact(contact_id)
    return {"contact": contact}


@app.get("/contacts/fname/{fname}")
def read_contacts_by_fname(fname: str):
    """Get contacts by first name."""
    if not service:
        return {"Error": "Data store service not set"}
    contacts = service.get_contacts_by_fname(fname)
    return {"contacts": contacts}


@app.get("/contacts/phone/{phone_number}")
def read_contacts_by_phone_number(phone_number: str):
    """Get contacts by phone number."""
    if not service:
        return {"Error": "Data store service not set"}
    contacts = service.get_contacts_by_phone_number(phone_number)
    return {"contacts": contacts}


@app.get("/contacts/email/{email}")
def read_contacts_by_email(email: str):
    """Get contacts by email."""
    if not service:
        return {"Error": "Data store service not set"}
    contacts = service.get_contacts_by_email(email)
    return {"contacts": contacts}


@app.get("/contacts/country/{country}")
def read_contacts_by_country(country: str):
    """Get contacts by country."""
    if not service:
        return {"Error": "Data store service not set"}
    contacts = service.get_contacts_by_country(country)
    return {"contacts": contacts}


@app.get("/contacts/state/{state}")
def read_contacts_by_state(state: str):
    """Get contacts by state."""
    if not service:
        return {"Error": "Data store service not set"}
    contacts = service.get_contacts_by_state(state)
    return {"contacts": contacts}

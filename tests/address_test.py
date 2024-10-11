import pytest

from contactlookup.models.address import Address

STREET = "123 Main St"
CITY = "Anytown"
STATE = "AnyState"
COUNTRY = "USA"
ZIP = "12345"
CONTACT_ID = 1
TYPE = "work"


@pytest.fixture
def addressfixture():
    return [STREET, CITY, STATE, ZIP, CONTACT_ID, TYPE, COUNTRY]


def test_address(addressfixture):
    address = Address(*addressfixture)

    assert address.street == STREET
    assert address.city == CITY.upper()
    assert address.state == STATE.upper()
    assert address.postal_code == ZIP
    assert address.contact_id == CONTACT_ID
    assert address.type == TYPE.upper()
    assert address.country == COUNTRY.upper()
    assert address.id is None

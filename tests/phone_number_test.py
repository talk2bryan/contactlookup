import pytest

from contact_lookup.models.phone_number import PhoneNumber

PHONE = "555-555-5555"
TYPE = "work"
CONTACT_ID = 1


@pytest.fixture
def phonefixture():
    return [PHONE, CONTACT_ID, TYPE]


def test_phone(phonefixture):
    phone = PhoneNumber(*phonefixture)

    assert phone.number == "5555555555"
    assert phone.type == TYPE
    assert phone.contact_id == CONTACT_ID
    assert phone.id is None

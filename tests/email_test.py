"""Testing the Email model."""

import pytest

from contact_lookup.models.email import Email

# Constants
EMAIL = "hello@world.org"
TYPE = "work"
CONTACT_ID = 1


# Create a test fixture
@pytest.fixture
def emailfixture():
    return [EMAIL, TYPE, CONTACT_ID]


def test_email(emailfixture):
    e_mail = Email(*emailfixture)

    assert e_mail.email == EMAIL
    assert e_mail.type == TYPE
    assert e_mail.contact_id == CONTACT_ID
    assert e_mail.id is None

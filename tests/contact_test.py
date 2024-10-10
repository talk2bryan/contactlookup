from contactlookup.models.address import Address
from contactlookup.models.contact import Contact
from contactlookup.models.email import Email
from contactlookup.models.phone_number import PhoneNumber


def test_new_contact_no_other_names():

    contact = Contact(1, "John", "Doe", None, "ACME", "CEO")

    assert contact.first_name == "John".upper()
    assert contact.last_name == "Doe".upper()
    assert contact.other_names is None
    assert contact.company == "ACME"
    assert contact.title == "CEO".upper()
    assert contact.nickname is None
    assert contact.phone_numbers == []
    assert contact.addresses == []
    assert contact.emails == []


def test_new_contact_with_other_names():

    contact = Contact(1, "John", "Doe", "Jacob Stacks", "ACME", "CEO")

    assert contact.first_name == "John".upper()
    assert contact.last_name == "Doe".upper()
    assert contact.other_names == "Jacob Stacks".upper()
    assert contact.company == "ACME"
    assert contact.title == "CEO".upper()
    assert contact.nickname is None
    assert contact.phone_numbers == []
    assert contact.addresses == []
    assert contact.emails == []


def test_add_phone_number():

    contact = Contact(1, "John", "Doe", None, "ACME", "CEO")
    phone = PhoneNumber("555-555-5555", 1, "work")

    contact.add_phone_number(phone)

    assert contact.phone_numbers == [phone]


def test_add_address():

    contact = Contact(1, "John", "Doe", None, "ACME", "CEO")
    address = Address("123 Main St", "Anytown", "AnyState", "12345", 1, "work", "USA")

    contact.add_address(address)

    assert contact.addresses == [address]


def test_add_email():

    contact = Contact(1, "John", "Doe", None, "ACME", "CEO")

    email = Email("hello@world.org", "work", contact.id)

    contact.add_email(email)

    assert contact.emails == [email]


def test_contact_equality():

    contact1 = Contact(1, "John", "Doe", None, "ACME", "CEO")
    contact2 = Contact(1, "John", "Doe", None, "ACME", "CEO")

    assert contact1 == contact2

    contact3 = Contact(1, "John", "Doe", None, "ACME", "CEO")
    contact4 = Contact(1, "John", "Doe", "Jacob Stacks", "ACME", "CEO")

    assert contact3 != contact4

    # Test that the __eq__ method works with lists
    contact_list = [contact1, contact3]
    assert contact1 in contact_list
    assert contact3 in contact_list
    assert contact4 not in contact_list

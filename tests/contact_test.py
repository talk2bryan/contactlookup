from contact_lookup.models.address import Address
from contact_lookup.models.contact import Contact
from contact_lookup.models.email import Email
from contact_lookup.models.phone_number import PhoneNumber


def test_new_contact_no_other_names():

    contact = Contact("John", "Doe", None, "ACME", "CEO")

    assert contact.first_name == "John"
    assert contact.last_name == "Doe"
    assert contact.other_names is None
    assert contact.company == "ACME"
    assert contact.title == "CEO"
    assert contact.nickname is None
    assert contact.phone_numbers == []
    assert contact.addresses == []
    assert contact.emails == []


def test_new_contact_with_other_names():

    contact = Contact("John", "Doe", "Jacob Stacks", "ACME", "CEO")

    assert contact.first_name == "John"
    assert contact.last_name == "Doe"
    assert contact.other_names == "Jacob Stacks"
    assert contact.company == "ACME"
    assert contact.title == "CEO"
    assert contact.nickname is None
    assert contact.phone_numbers == []
    assert contact.addresses == []
    assert contact.emails == []


def test_add_phone_number():

    contact = Contact("John", "Doe", None, "ACME", "CEO")
    phone = PhoneNumber("555-555-5555", 1, "work")

    contact.add_phone_number(phone)

    assert contact.phone_numbers == [phone]


def test_add_address():
    from contact_lookup.models.contact import Contact

    contact = Contact("John", "Doe", None, "ACME", "CEO")
    address = Address("123 Main St", "Anytown", "AnyState", "12345", 1, "work", "USA")

    contact.add_address(address)

    assert contact.addresses == [address]


def test_add_email():
    from contact_lookup.models.contact import Contact

    contact = Contact("John", "Doe", None, "ACME", "CEO")
    contact.id = 1

    email = Email("hello@world.org", "work", contact.id)

    contact.add_email(email)

    assert contact.emails == [email]

import pytest

from contactlookup.definitions import SAMPLE_CONTACTS_DIR, SAMPLE_CONTACTS_FILE
from contactlookup.models.contact import Contact
from contactlookup.services.file_data_store_service import (
    ContactBST,
    ContactNode,
    FileDataStoreService,
)


def test_contact_node_one_contact():
    contact = Contact(1, "John", "Doe", None, "ACME", "CEO")
    node = ContactNode(contact.first_name)

    assert node.key == "John".upper()
    assert not node.contacts

    node.add_contact(contact)

    assert node.contacts == [contact]
    assert node.left is None
    assert node.right is None


def test_contact_node_multiple_contacts_sorted():
    contact1 = Contact(1, "John", "Doe", None, "ACME", "CEO")
    contact2 = Contact(2, "John", "Deux", None, "ACME", "CEO")
    node = ContactNode(contact1.first_name)

    node.add_contact(contact1)
    node.add_contact(contact2)

    # Sort order is maintained
    assert node.contacts == [contact2, contact1]
    assert node.left is None
    assert node.right is None


def test_contact_node_with_left_child():
    contact1 = Contact(1, "John", "Doe", None, "ACME", "CEO")
    contact2 = Contact(2, "Jane", "Doe", None, "ACME", "CEO")
    john_node = ContactNode(contact1.first_name)
    jane_node = ContactNode(contact2.first_name)

    john_node.add_contact(contact1)
    jane_node.add_contact(contact2)

    john_node.left = jane_node

    assert john_node.contacts == [contact1]
    assert john_node.left.contacts == [contact2]
    assert john_node.right is None


def test_contact_bst_insert_root():
    contact = Contact(1, "John", "Doe", None, "ACME", "CEO")
    bst = ContactBST()

    bst.insert(contact)

    assert bst.root.contacts == [contact]
    assert bst.root.left is None
    assert bst.root.right is None


def test_contact_bst_insert_left():
    contact1 = Contact(1, "John", "Doe", None, "ACME", "CEO")
    contact2 = Contact(2, "Jane", "Doe", None, "ACME", "CEO")
    bst = ContactBST()

    bst.insert(contact1)
    bst.insert(contact2)

    assert bst.root.contacts == [contact1]
    assert bst.root.left.contacts == [contact2]
    assert bst.root.right is None


def test_contact_bst_insert_right():
    contact1 = Contact(1, "John", "Doe", None, "ACME", "CEO")
    contact2 = Contact(1, "Jane", "Doe", None, "ACME", "CEO")
    bst = ContactBST()

    bst.insert(contact2)
    bst.insert(contact1)

    assert bst.root.contacts == [contact2]
    assert bst.root.left is None
    assert bst.root.right.contacts == [contact1]


def test_contact_bst_insert_left_right():
    contact1 = Contact(1, "John", "Doe", None, "ACME", "CEO")
    contact2 = Contact(2, "Jane", "Doe", None, "ACME", "CEO")
    contact3 = Contact(3, "Jill", "Doe", None, "ACME", "CEO")
    bst = ContactBST()

    bst.insert(contact2)
    bst.insert(contact1)
    bst.insert(contact3)

    # Jane is the root, John is the right child, Jill is the left child of John
    #         Jane
    #             \
    #             John
    #            /
    #         Jill
    assert bst.root.contacts == [contact2]
    assert bst.root.right.contacts == [contact1]
    assert bst.root.right.left.contacts == [contact3]


def test_contact_bst_insert_same_level():
    contact1 = Contact(1, "John", "Doe", None, "ACME", "CEO")
    contact2 = Contact(2, "Jane", "Doe", None, "ACME", "CEO")
    contact3 = Contact(3, "Jill", "Doe", None, "ACME", "CEO")
    contact4 = Contact(4, "Jack", "Doe", None, "ACME", "CEO")
    bst = ContactBST()

    bst.insert(contact2)
    bst.insert(contact1)
    bst.insert(contact3)
    bst.insert(contact4)

    # Jane is the root, John is the right child, Jill is the left child of John
    #         Jane
    #        /     \
    #      Jack     John
    #            /
    #         Jill
    assert bst.root.contacts == [contact2]
    assert bst.root.right.contacts == [contact1]
    assert bst.root.right.left.contacts == [contact3]
    assert bst.root.left.contacts == [contact4]


def test_contact_bst_insert_same_fname():
    contact1 = Contact(1, "John", "Doe", None, "ACME", "CEO")
    contact2 = Contact(2, "John", "Deux", None, "ACME", "CEO")
    contact3 = Contact(3, "John", "Drei", None, "ACME", "CEO")
    contact4 = Contact(4, "Jane", "Doe", None, "ACME", "CEO")
    contact5 = Contact(5, "Jane", "Deux", None, "ACME", "CEO")
    bst = ContactBST()

    # Johns are stored in the root, Janes are stored in the left child
    #              John
    #  (John Deux, John Doe, John Drei) - order is maintained by last name
    #           /
    #       Jane
    # (Jane Deux, Jane Doe)
    # Inserting in non-ascending order to test sorting
    bst.insert(contact1)
    bst.insert(contact2)
    bst.insert(contact4)
    bst.insert(contact3)
    bst.insert(contact5)

    assert bst.root.contacts == [contact2, contact1, contact3]
    assert bst.root.left.contacts == [contact5, contact4]


@pytest.mark.datafiles(SAMPLE_CONTACTS_DIR)
def test_file_data_store_service_load_contacts(datafiles):
    service = FileDataStoreService()
    service.set_contacts_file_path(datafiles / SAMPLE_CONTACTS_FILE)

    success = service.initialize()
    assert success is True

    # Test that the attributes are correct
    all_contacts = service.get_contacts()
    assert len(all_contacts) == 4

    contact = all_contacts[0]
    assert contact.first_name == "Kristen".upper()

    contact = service.all_contacts[1]
    assert contact.first_name == "Karla".upper()

    contact = service.all_contacts[2]
    assert contact.first_name == "Jeff".upper()

    # Test that get_contact works
    # Since there are 4 contacts, the valid IDs are 1, 2, 3, 4
    contact = service.get_contact(0)
    assert contact is None

    contact = service.get_contact(5)
    assert contact is None

    contact = service.get_contact(1)
    assert contact.first_name == "Kristen".upper()

    contact = service.get_contact(4)
    assert contact.first_name == "Jeff".upper()

    # Test that get_contacts_by_fname works
    contacts = service.get_contacts_by_fname("Kristen")
    assert len(contacts) == 1
    # There are 2 contacts with the first name "Jeff"
    contacts = service.get_contacts_by_fname("Jeff")
    assert len(contacts) == 2

    # Test that get_contacts_by_phone_number works
    contacts = service.get_contacts_by_phone_number("+363-214-4414254")
    assert len(contacts) == 1

    # Check for a phone number that doesn't exist
    contacts = service.get_contacts_by_phone_number("555-555-5555")
    assert len(contacts) == 0

    # Test that get_contacts_by_email works
    contacts = service.get_contacts_by_email("allentaylor@example.net")
    assert len(contacts) == 1

    # Test that get_contacts_by_email is case-insensitive
    contacts = service.get_contacts_by_email("ALLENTAYLOR@EXAMPLE.NET")
    assert len(contacts) == 1

    # Test for an email that doesn't exist
    contacts = service.get_contacts_by_email("test@example.net")
    assert len(contacts) == 0

    # Check that get_contacts_by_country works
    contacts = service.get_contacts_by_country("USA")
    # There are 2 contacts with the country "USA"
    assert len(contacts) == 2

    contacts = service.get_contacts_by_country("usa")
    assert len(contacts) == 2

    # Test that get_contacts_by_state works
    contacts = service.get_contacts_by_state("CA")

    # There are 2 contacts with the state "CA"
    assert len(contacts) == 2

    # Test that get_contacts_by_state is case-insensitive
    contacts = service.get_contacts_by_state("ca")
    assert len(contacts) == 2

    # Test for a state that doesn't exist
    contacts = service.get_contacts_by_state("NY")
    assert len(contacts) == 0

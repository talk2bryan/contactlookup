"""Design decisions for the file data store service.

We want to be able to search by the following criteria:
    - ID
    - Name (first name) - most common search criteria
    - Phone number
    - Email
    - State
    - Country

Data structures:
We will save the contacts in different data structures to allow for efficient
searching by the different criteria. This will be done in the initialize method.

* all_contacts: list[Contact] where the index is the contact ID.
* contacts_by_name: BST where the key is the first name.
* contacts_by_phone_number: dict where the key is the phone number.
* contacts_by_email: dict where the key is the email.
* contacts_by_state: dict where the key is the state, and the value is a list of
    contacts.
* contacts_by_country: dict where the key is the country, and the value is a list
    of contacts.
"""

import logging
from collections.abc import Generator
from pathlib import Path

import vobject

from contact_lookup.definitions import VCF_EXTENSION
from contact_lookup.models.address import Address
from contact_lookup.models.contact import Contact
from contact_lookup.models.email import Email
from contact_lookup.models.phone_number import PhoneNumber
from contact_lookup.services.data_store_service import DataStoreService


class ContactNode:
    """Contact node for the BST, allowing for multiple contacts with the same key.

    Using a BST allows for O(log n) search time. The key is the first name of
    the contact. The contacts list contains all the contacts with the same first
    name. The contacts are sorted by last name. The decision to use the first
    name as the key is because it is the most common search criteria. Therefore,
    the height of the tree will be minimized.
    """

    def __init__(self, key: str):
        self.key = key
        self.contacts: list[Contact] = []
        self.left: ContactNode | None = None
        self.right: ContactNode | None = None

    def add_contact(self, contact: Contact):
        if contact not in self.contacts:
            self.contacts.append(contact)
            self.contacts.sort(key=lambda x: x.last_name)


class ContactBST:
    """Contact Binary Search Tree."""

    def __init__(self):
        self.root: ContactNode | None = None

    def insert(self, contact: Contact):
        if self.root is None:
            self.root = ContactNode(contact.first_name)
            self.root.add_contact(contact)
        else:
            self._insert(self.root, contact)

    def _insert(self, node: ContactNode, contact: Contact):
        if node.key == contact.first_name:
            node.add_contact(contact)
        elif contact.first_name < node.key:
            if node.left is None:
                node.left = ContactNode(contact.first_name)
                node.left.add_contact(contact)
            else:
                self._insert(node.left, contact)
        else:
            if node.right is None:
                node.right = ContactNode(contact.first_name)
                node.right.add_contact(contact)
            else:
                self._insert(node.right, contact)

    def get_contacts_with_fname(self, first_name: str) -> list:
        if self.root is None:
            return []

        return self._get_contacts_with_fname(self.root, first_name)

    def _get_contacts_with_fname(
        self,
        node: ContactNode | None,
        first_name: str,
    ) -> list:
        if node is None:
            return []

        if first_name == node.key:
            return node.contacts
        elif first_name < node.key:
            return self._get_contacts_with_fname(node.left, first_name)
        else:
            return self._get_contacts_with_fname(node.right, first_name)


class FileDataStoreService(DataStoreService):
    """File data store service."""

    # Default contact ID. This will be incremented for each contact.
    contact_id: int = 0

    def __init__(self):
        self._contacts_file_path: Path | None = None
        self._validated_file_path: bool = False
        self.all_contacts: list[Contact] = []
        self.contacts_by_name: ContactBST = ContactBST()
        self.contacts_by_phone_number: dict[str, Contact] = {}
        self.contacts_by_email: dict[str, Contact] = {}
        self.contacts_by_state: dict[str, list[Contact]] = {}
        self.contacts_by_country: dict[str, list[Contact]] = {}

    @classmethod
    def parse_contact_dict(cls, contact_dict: dict[str, list]) -> Contact | None:
        """Parse a contact dictionary."""

        logger = logging.getLogger(__name__)
        cls.contact_id += 1
        try:
            fields = contact_dict.keys()
            fields_of_interest = [
                "fn",
                "org",
                "title",
                "nickname",
                "bday",
                "tel",
                "email",
                "adr",
            ]

            # Create a contact with the required fields using placeholder values
            contact: Contact = Contact(
                id=cls.contact_id,
                first_name="",
                last_name="",
                other_names=None,
                company=None,
                title=None,
            )
            emails: list[Email] = []
            phone_numbers: list[PhoneNumber] = []
            addresses: list[Address] = []

            for field in fields_of_interest:
                if field not in fields:
                    continue
                if field == "fn":
                    full_name: str = contact_dict[field][0].value
                    parts: list[str] = full_name.strip().split()
                    first_name: str = parts[0]
                    last_name: str = parts[-1] if len(parts) > 1 else ""
                    other_names: str | None = (
                        " ".join(parts[1:-1]) if len(parts) > 2 else None
                    )

                    contact.first_name = first_name
                    contact.last_name = last_name
                    contact.other_names = other_names
                elif field == "org":
                    company: str | None = contact_dict[field][0].value[0].strip()
                    company = company if company != "None" else None

                    contact.company = company
                elif field == "title":
                    title: str | None = contact_dict[field][0].value.strip()
                    title = title if title != "None" else None

                    contact.title = title
                elif field == "nickname":
                    nickname: str | None = contact_dict[field][0].value.strip()
                    nickname = nickname if nickname != "None" else None

                    contact.nickname = nickname
                elif field == "bday":
                    birthday: str | None = contact_dict[field][0].value.strip()
                    birthday = birthday if birthday != "None" else None

                    contact.birthday = birthday
                elif field == "tel":
                    # Multiple phone numbers can be present
                    for phone in contact_dict[field]:
                        phone_number: str = phone.value
                        phone_type: str | None = phone.params.get("type")
                        phone_numbers.append(
                            PhoneNumber(
                                number=phone_number,
                                contact_id=cls.contact_id,
                                type=phone_type,
                            ),
                        )
                elif field == "email":
                    # Multiple emails can be present
                    for email in contact_dict[field]:
                        email_address: str = email.value
                        email_type: str | None = email.params.get("type")
                        emails.append(
                            Email(
                                email=email_address,
                                type=email_type,
                                contact_id=cls.contact_id,
                            ),
                        )
                elif field == "adr":
                    # Multiple addresses can be present
                    for address in contact_dict[field]:
                        street: str = address.value.street.strip()
                        if not street or street == "None":
                            # Required field
                            continue

                        city: str | None = address.value.city
                        city = city.strip() if city and city.strip() != "None" else None
                        state: str | None = address.value.region
                        state = (
                            state.strip() if state and state.strip() != "None" else None
                        )
                        postal_code: str | None = address.value.code
                        postal_code = (
                            postal_code.strip()
                            if postal_code and postal_code.strip() != "None"
                            else None
                        )
                        country: str | None = address.value.country
                        country = (
                            country.strip()
                            if country and country.strip() != "None"
                            else None
                        )
                        address_type: str | None = address.params.get("type")
                        address_type = address_type.strip() if address_type else None

                        addresses.append(
                            Address(
                                street=street,
                                city=city,
                                state=state,
                                postal_code=postal_code,
                                contact_id=cls.contact_id,
                                type=address_type,
                                country=country,
                            ),
                        )
            # Ensure all contact fields are properly formatted
            contact.refresh()
            # Add the phone numbers, emails, and addresses to the contact
            contact.phone_numbers.extend(phone_numbers)
            contact.emails.extend(emails)
            contact.addresses.extend(addresses)
            return contact
        except AttributeError as e:
            logger.error("parse_contact_dict|AttributeError: %s", e)
            # Reset the contact ID since the contact was not created
            cls.contact_id -= 1
            return None
        except IndexError as e:
            logger.error("parse_contact_dict|IndexError: %s", e)
            # Reset the contact ID since the contact was not created
            cls.contact_id -= 1
            return None

    @classmethod
    def read_vcf_file(
        cls,
        file_path: Path,
        logger: logging.Logger,
    ) -> Generator[Contact, None, None]:
        """Read a VCF file and yield contacts."""
        try:
            obj = vobject.readComponents(
                file_path.read_text(encoding="utf-8", errors="ignore"),
            )
        except OSError as e:
            logger.error("read_vcf_file|IOError: %s", e)
            return

        logger.info("read_vcf_file|Parsing contacts.")

        try:
            for component in obj:
                try:
                    component_dict: dict[str, list] = dict(component.contents)
                    contact = cls.parse_contact_dict(component_dict)
                    if not contact:
                        continue
                    yield contact
                except AttributeError as e:
                    logger.error("read_vcf_file|AttributeError: %s", e)
                    continue
        except vobject.base.ParseError as e:
            logger.error("read_vcf_file|ParseError: %s", e)
            return
        except Exception as e:
            logger.error("read_vcf_file|Error: %s", e)
            return

    def set_contacts_file_path(self, file_path: Path):
        """Set the contacts file path."""
        valid_file: bool = True
        if not file_path.exists():
            valid_file = False
        elif not file_path.is_file():
            valid_file = False
        elif not file_path.suffix == VCF_EXTENSION:
            valid_file = False
        if valid_file:
            self._contacts_file_path = file_path
            self._validated_file_path = True

    def initialize(self) -> bool:
        """Initialize data store."""
        logger = logging.getLogger(__name__)
        logger.info("initialize|Initializing file data store.")

        # True if
        # - the file path is valid
        # - the file is read successfully
        # - the file is parsed successfully
        # - the contacts are indexed successfully
        success: bool = False
        if not self._validated_file_path:
            logger.error("initialize|Contacts file path not validated.")
            return success
        try:

            assert self._contacts_file_path, "Contacts file path not set."
        except AssertionError as e:
            logger.error("initialize|Error: %s", e)
            return success
        contacts = self.read_vcf_file(file_path=self._contacts_file_path, logger=logger)
        if not contacts:
            logger.error("initialize|No contacts read.")
            return success
        # Index contacts
        try:

            for contact in contacts:
                self.all_contacts.append(contact)
                self.contacts_by_name.insert(contact)
                for phone_number in contact.phone_numbers:
                    self.contacts_by_phone_number[phone_number.number] = contact
                for email in contact.emails:
                    self.contacts_by_email[email.email] = contact
                for address in contact.addresses:
                    if address.state:
                        if address.state not in self.contacts_by_state:
                            self.contacts_by_state[address.state] = []
                        self.contacts_by_state[address.state].append(contact)
                    if address.country:
                        if address.country not in self.contacts_by_country:
                            self.contacts_by_country[address.country] = []
                        self.contacts_by_country[address.country].append(contact)
        except Exception as e:
            logger.error("initialize|Error indexing contacts: %s", e)
            return success

        success = True
        logger.info("initialize|File data store initialized successfully.")
        return success

    def get_contact(self, contact_id: int) -> Contact | None:
        """Get contact by ID."""
        size = len(self.all_contacts)

        if (size > 0 and contact_id > 0) and contact_id <= size:
            return self.all_contacts[contact_id - 1]
        return None

    def get_contacts(self) -> list[Contact]:
        """Get all contacts."""
        return self.all_contacts

    def get_contacts_by_fname(self, fname: str) -> list:
        """Get contacts by first name."""
        return self.contacts_by_name.get_contacts_with_fname(fname.upper())

    def get_contacts_by_phone_number(self, phone_number: str) -> list:
        """Get contacts by phone number."""
        # Clean up the phone number
        phone_number = (
            phone_number.strip()
            .replace("-", "")
            .replace(" ", "")
            .replace("(", "")
            .replace(")", "")
            .replace("+", "")
            .replace(".", "")
        )
        # TODO: At some point, we may want to allow for partial matches.
        contact = self.contacts_by_phone_number.get(phone_number)
        if contact:
            return [contact]
        return []

    def get_contacts_by_email(self, email: str) -> list:
        """Get contacts by email."""
        contact = self.contacts_by_email.get(email.strip().lower())
        if contact:
            return [contact]
        return []

    def get_contacts_by_country(self, country: str) -> list:
        """Get contacts by country."""
        contacts = self.contacts_by_country.get(country.strip().upper())
        if contacts:
            return contacts
        return []

    def get_contacts_by_state(self, state: str) -> list:
        """Get contacts by state."""
        contacts = self.contacts_by_state.get(state.strip().upper())
        if contacts:
            return contacts
        return []

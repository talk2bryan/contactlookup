"""Abstract class for data store service."""

from abc import ABC, abstractmethod

from contactlookup.models.contact import Contact


class DataStoreService(ABC):
    """Abstract class for data store service."""

    @abstractmethod
    def initialize(self) -> bool:
        """Initialize data store."""

    @abstractmethod
    def get_contact(self, contact_id: int) -> Contact | None:
        """Get contact by ID."""

    @abstractmethod
    def get_contacts(self) -> list[Contact]:
        """Get all contacts."""

    @abstractmethod
    def get_contacts_by_fname(self, fname: str) -> list:
        """Get contacts by first name."""

    @abstractmethod
    def get_contacts_by_phone_number(self, phone_number: str) -> list:
        """Get contacts by phone number."""

    @abstractmethod
    def get_contacts_by_email(self, email: str) -> list:
        """Get contacts by email."""

    @abstractmethod
    def get_contacts_by_country(self, country: str) -> list:
        """Get contacts by country."""

    @abstractmethod
    def get_contacts_by_state(self, state: str) -> list:
        """Get contacts by state."""

    # Write operations are not needed for this project
    # @abstractmethod
    # def create_contact(self, contact: dict) -> dict:
    #     """Create a new contact."""

    # @abstractmethod
    # def update_contact(self, contact_id: str, contact: dict) -> dict:
    #     """Update contact by ID."""

    # @abstractmethod
    # def delete_contact(self, contact_id: str) -> dict:
    #     """Delete contact by ID."""

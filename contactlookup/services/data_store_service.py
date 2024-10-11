"""Abstract class for data store service."""

from abc import ABC, abstractmethod

from contactlookup.models.contact import Contact


class DataStoreService(ABC):
    """Abstract class for data store service."""

    @abstractmethod
    def initialize(self) -> bool:
        """Initialize data store."""
        pass

    @abstractmethod
    def get_contact(self, contact_id: int) -> Contact | None:
        """Get contact by ID."""
        pass

    @abstractmethod
    def get_contacts(self) -> list[Contact]:
        """Get all contacts."""
        pass

    @abstractmethod
    def get_contacts_by_fname(self, fname: str) -> list:
        """Get contacts by first name."""
        pass

    @abstractmethod
    def get_contacts_by_phone_number(self, phone_number: str) -> list:
        """Get contacts by phone number."""
        pass

    @abstractmethod
    def get_contacts_by_email(self, email: str) -> list:
        """Get contacts by email."""
        pass

    @abstractmethod
    def get_contacts_by_country(self, country: str) -> list:
        """Get contacts by country."""
        pass

    @abstractmethod
    def get_contacts_by_state(self, state: str) -> list:
        """Get contacts by state."""
        pass

    # Write operations are not needed for this project
    # @abstractmethod
    # def create_contact(self, contact: dict) -> dict:
    #     """Create a new contact."""
    #     pass

    # @abstractmethod
    # def update_contact(self, contact_id: str, contact: dict) -> dict:
    #     """Update contact by ID."""
    #     pass

    # @abstractmethod
    # def delete_contact(self, contact_id: str) -> dict:
    #     """Delete contact by ID."""
    #     pass

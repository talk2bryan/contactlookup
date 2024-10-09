# A VCF contact model
from dataclasses import dataclass, field

from contact_lookup.models.address import Address
from contact_lookup.models.email import Email
from contact_lookup.models.phone_number import PhoneNumber


@dataclass
class Contact:
    id: int
    first_name: str
    last_name: str
    other_names: str | None
    company: str | None
    title: str | None
    nickname: str | None = field(default=None)
    birthday: str | None = field(default=None)
    phone_numbers: list[PhoneNumber] = field(default_factory=list)
    addresses: list[Address] = field(default_factory=list)
    emails: list[Email] = field(default_factory=list)

    def __post_init__(self):
        self.first_name = self.first_name.strip().upper()
        self.last_name = self.last_name.strip().upper()
        self.company = self.company.strip() if self.company is not None else None
        self.title = self.title.strip().upper() if self.title is not None else None
        self.other_names = (
            self.other_names.strip().upper() if self.other_names is not None else None
        )
        self.nickname = (
            self.nickname.strip().upper() if self.nickname is not None else None
        )

    def __eq__(self, other):
        if not isinstance(other, Contact):
            return False

        return (
            self.first_name == other.first_name
            and self.last_name == other.last_name
            and self.other_names == other.other_names
            and self.company == other.company
            and self.title == other.title
            and self.nickname == other.nickname
            and self.phone_numbers == other.phone_numbers
            and self.addresses == other.addresses
            and self.emails == other.emails
        )

    def add_phone_number(self, phone_number: PhoneNumber):
        self.phone_numbers.append(phone_number)

    def add_address(self, address: Address):
        self.addresses.append(address)

    def add_email(self, email: Email):
        self.emails.append(email)

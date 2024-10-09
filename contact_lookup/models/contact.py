# A VCF contact model
from dataclasses import dataclass, field

from contact_lookup.models.address import Address
from contact_lookup.models.email import Email
from contact_lookup.models.phone_number import PhoneNumber


@dataclass
class Contact:
    id: int | None = field(init=False, default=None)
    first_name: str
    last_name: str
    other_names: str | None
    company: str | None
    title: str | None
    nickname: str | None = field(default=None)
    phone_numbers: list[PhoneNumber] = field(default_factory=list)
    addresses: list[Address] = field(default_factory=list)
    emails: list[Email] = field(default_factory=list)

    def __post_init__(self):
        self.first_name = self.first_name.strip()
        self.last_name = self.last_name.strip()
        self.company = self.company.strip() if self.company is not None else None
        self.title = self.title.strip() if self.title is not None else None
        self.other_names = (
            self.other_names.strip() if self.other_names is not None else None
        )
        self.nickname = self.nickname.strip() if self.nickname is not None else None

    def add_phone_number(self, phone_number: PhoneNumber):
        self.phone_numbers.append(phone_number)

    def add_address(self, address: Address):
        self.addresses.append(address)

    def add_email(self, email: Email):
        self.emails.append(email)

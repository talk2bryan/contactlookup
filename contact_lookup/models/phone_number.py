from dataclasses import dataclass, field


@dataclass
class PhoneNumber:
    id: int | None = field(init=False, default=None)
    phone_number: str
    contact_id: int
    type: str | None = field(default=None)

    def __post_init__(self):
        # Remove all spaces, dashes, and parentheses from the phone number
        self.phone_number = "".join(
            [char for char in self.phone_number if char.isnumeric() or char == "+"],
        )

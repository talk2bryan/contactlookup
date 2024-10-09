from dataclasses import dataclass, field


@dataclass
class PhoneNumber:
    id: int | None = field(init=False, default=None)
    number: str
    contact_id: int
    type: str | None = field(default=None)

    def __post_init__(self):
        # Remove all spaces, dashes, parentheses and + from the phone number
        self.number = "".join(
            [char for char in self.number if char.isnumeric()],
        )
        self.type = self.type.strip().upper() if self.type is not None else None

from dataclasses import dataclass, field


@dataclass
class Address:
    id: int | None = field(init=False, default=None)
    street: str
    city: str | None
    state: str | None
    postal_code: str | None
    contact_id: int
    type: str | None = None
    country: str | None = None

    def __post_init__(self):
        self.street = self.street.strip()
        self.city = self.city.strip() if self.city is not None else None
        self.state = self.state.strip() if self.state is not None else None
        self.postal_code = (
            self.postal_code.strip() if self.postal_code is not None else None
        )
        self.country = self.country.strip() if self.country is not None else None
        self.type = self.type.strip() if self.type is not None else None

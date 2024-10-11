from dataclasses import dataclass, field


@dataclass
class Email:
    id: int | None = field(init=False, default=None)
    email: str
    type: str | None
    contact_id: int

    def __post_init__(self):
        self.email = self.email.strip()
        self.type = self.type.strip().lower() if self.type is not None else None

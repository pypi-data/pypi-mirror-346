from typing import Optional

from ed_domain.core.entities.consumer import Consumer
from pydantic import BaseModel


class ConsumerDto(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    email: Optional[str]

    @classmethod
    def from_consumer(cls, consumer: Consumer) -> "ConsumerDto":
        return cls(
            first_name=consumer["first_name"],
            last_name=consumer["last_name"],
            phone_number=consumer["phone_number"],
            email=consumer["email"],
        )

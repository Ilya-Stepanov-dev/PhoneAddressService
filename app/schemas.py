from pydantic import BaseModel
from app.types import RussianPhone

class PhoneAddress(BaseModel):
    phone: RussianPhone
    address: str

    class Config:
        json_schema_extra = {
            "example": {
                "phone": "+79991234567",
                "address": "Moscow, Lenina street, 12"
            }
        }

class Address(BaseModel):
    address: str

    class Config:
        json_schema_extra = {
            "example": {
                "address": "Moscow, Lenina street, 12"
            }
        }

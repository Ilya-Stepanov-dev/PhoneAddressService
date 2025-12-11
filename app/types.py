import re
from typing import Annotated
from pydantic import PlainValidator

from app.exceptions import InvalidPhoneFormatError

def validate_russian_phone(value: str) -> str:
    """
    Validate Russian phone number
    """

    if not isinstance(value, str):
        raise InvalidPhoneFormatError(
            phone=value,
            detail="Number must be a string",
        )

    phone = re.sub(r'[^\d+]', '', value)
    phone = phone.lstrip('+')

    if not phone.isdigit():
        raise InvalidPhoneFormatError(
            phone=value,
            detail="Number must contain only digits",
        )

    if phone.startswith('7'):
        phone = '8' + phone[1:]
    elif not phone.startswith('8'):
        raise InvalidPhoneFormatError(
            phone=value,
            detail="Number must start with 8 or +7",
        )

    if len(phone) != 11:
        raise InvalidPhoneFormatError(
            phone=value,
            detail=f"Number must be 11 digits, not {len(phone)}",
        )

    return phone

RussianPhone = Annotated[str, PlainValidator(validate_russian_phone)]

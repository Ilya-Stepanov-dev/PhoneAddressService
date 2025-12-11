from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from app.schemas import PhoneAddress, Address
from app.services import PhoneAddressService
from app.depends import get_phone_service
from app.types import RussianPhone
from app.routes.response import (
    r_200_UPDATE,
    r_201_CREATED,
    r_204_NO_CONTENT,
    r_404_NOT_FOUND,
    r_409_CONFLICT,
)

router = APIRouter(
    prefix="/phone",
    tags=["Phone Address Management"]
)


@router.get(
    "/{phone}",
    response_model=Address,
    status_code=status.HTTP_200_OK,
    responses={
        r_404_NOT_FOUND.code: r_404_NOT_FOUND.doc,
    }
)
async def get_phone_address(
    phone: RussianPhone,
    service: PhoneAddressService = Depends(get_phone_service),
):
    """
    Get phone address by phone number.

    Args:
        phone (RussianPhone): Phone number.

    Returns:
        Address: Phone address.

    Raises:
        PhoneNotFoundError: If phone number not found.
    """
    address = await service.get_address(phone)

    return Address(
        address=address
    )

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    responses = {
        r_201_CREATED.code: r_201_CREATED.doc,
        r_409_CONFLICT.code: r_409_CONFLICT.doc,
    }
)
async def create_phone_address(
    data: PhoneAddress,
    service: PhoneAddressService = Depends(get_phone_service),
):
    """
    Create phone address mapping.

    Args:
        data (PhoneAddress): Phone address mapping.

    Returns:
        JSONResponse: Created response.

    Raises:
        PhoneAlreadyExistsError: If phone number already exists.
    """
    await service.create_address(data.phone, data.address)

    return r_201_CREATED.json()


@router.put(
    "/{phone}",
    status_code=status.HTTP_200_OK,
    responses = {
        r_200_UPDATE.code: r_200_UPDATE.doc,
        r_404_NOT_FOUND.code: r_404_NOT_FOUND.doc,
    }
)
async def update_phone_address(
    phone: RussianPhone,
    data: Address,
    service: PhoneAddressService = Depends(get_phone_service),
):
    """
    Update phone address mapping.

    Args:
        phone (RussianPhone): Phone number.
        data (Address): Phone address mapping.

    Returns:
        JSONResponse: Updated response.

    Raises:
        PhoneNotFoundError: If phone number not found.
    """
    await service.update_address(phone, data.address)

    return r_200_UPDATE.json()


@router.delete(
    "/{phone}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses = {
        r_204_NO_CONTENT.code: r_204_NO_CONTENT.doc,
        r_404_NOT_FOUND.code: r_404_NOT_FOUND.doc,
    }
)
async def delete_phone_address(
    phone: RussianPhone,
    service: PhoneAddressService = Depends(get_phone_service),
):
    """
    Delete phone address mapping.

    Args:
        phone (RussianPhone): Phone number.

    Returns:
        JSONResponse: Deleted response.

    Raises:
        PhoneNotFoundError: If phone number not found.
    """
    await service.delete_address(phone)

    return r_204_NO_CONTENT.json()

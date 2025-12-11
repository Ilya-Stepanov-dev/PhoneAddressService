from redis.asyncio import Redis
from app.config.config import redis_config
from app.exceptions import (
    PhoneNotFoundError,
    PhoneAlreadyExistsError,
)


class PhoneAddressService:
    KEY_PREFIX = "phone:"
    TTL = redis_config.TTL_PHONE

    def __init__(self, redis_connection: Redis):
        self.redis = redis_connection

    def _make_key(self, phone: str) -> str:
        return f"{self.KEY_PREFIX}{phone}"

    async def get_address(self, phone: str) -> str:
        """
        Get address by phone number.

        Args:
            phone (str): Phone number.

        Returns:
            str: Address.

        Raises:
            PhoneNotFoundError: If phone number not found.
        """
        key = self._make_key(phone)
        address = await self.redis.get(key)
        if address is None:
            raise PhoneNotFoundError(phone)
        return address

    async def create_address(self, phone: str, address: str) -> None:
        """
        Create phone address mapping.

        Args:
            phone (str): Phone number.
            address (str): Address.

        Raises:
            PhoneAlreadyExistsError: If phone number already exists.
        """
        key = self._make_key(phone)
        exists = await self.redis.exists(key)

        if exists:
            raise PhoneAlreadyExistsError(phone)

        await self.redis.setex(
            key,
            self.TTL,
            address
        )

    async def update_address(self, phone: str, address: str, save_ttl: bool = True) -> None:
        """
        Update phone address mapping.

        Args:
            phone (str): Phone number.
            address (str): Address.
            save_ttl (bool, optional): If True, save TTL for the key. Defaults to True.

        Raises:
            PhoneNotFoundError: If phone number not found.
        """

        key = self._make_key(phone)
        exists = await self.redis.exists(key)

        if not exists:
            raise PhoneNotFoundError(phone)

        if not save_ttl:
            await self.redis.setex(key, self.TTL, address)
            return

        ttl = await self.redis.ttl(key)
        if ttl == -1:
            ttl = self.TTL

        await self.redis.setex(key, ttl, address)

    async def delete_address(self, phone: str) -> None:
        """
        Delete phone address mapping.

        Args:
            phone (str): Phone number.

        Raises:
            PhoneNotFoundError: If phone number not found.
        """
        key = self._make_key(phone)
        deleted = await self.redis.delete(key)

        if deleted == 0:
            raise PhoneNotFoundError(phone)


    async def _exists(self, key: str) -> bool:
        exists = await self.redis.exists(key)
        return bool(exists)

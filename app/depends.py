from app.redis_manager import redis_manager
from app.services import PhoneAddressService

def get_phone_service():
    return PhoneAddressService(redis_manager.get_connection())

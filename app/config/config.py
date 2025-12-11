from pydantic_settings import BaseSettings

class RedisConfig(BaseSettings):
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    TTL_PHONE: int = 3600

    class Config:
        env_file = ".env"
        case_sensitive = True

class ServiceConfig(BaseSettings):
    APP_NAME: str = "Phone Address Service"
    APP_VERSION: str = "1.0.0"
    APP_LOG_LEVEL: str = "INFO"
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True

redis_config = RedisConfig()
service_config = ServiceConfig()

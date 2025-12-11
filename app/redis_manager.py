import logging
from redis.asyncio import Redis
from app.exceptions import RedisConnectionError
from app.config import redis_config

logger = logging.getLogger(__name__)

class RedisManager:
    def __init__(
            self,
            host: str = "localhost",
            port: int = 6379,
            db: int = 0
        ):
        self._host = host
        self._port = port
        self._db = db
        self._connection: Redis | None = None

    def _get_url(self):
        return f"redis://{self._host}:{self._port}/{self._db}"

    async def connect(self) -> None:
        try:
            self._connection = await Redis.from_url(self._get_url())
            await self._connection.ping()
            logger.info("Connection to Redis established successfully")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise RedisConnectionError(str(e))

    async def disconnect(self) -> None:
        if self._connection:
            await self._connection.close()
            logger.info("Connection to Redis closed")

    def get_connection(self) -> Redis | None:
        return self._connection

redis_manager = RedisManager(
    host=redis_config.REDIS_HOST,
    port=redis_config.REDIS_PORT,
    db=redis_config.REDIS_DB,
)

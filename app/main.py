import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.config import service_config
from app.routes import api_router
from app.exceptions import register_exceptions_handlers
from app.redis_manager import redis_manager

from app.config import setup_logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):

    async def on_startup():
        logger.info("Service started")
        await redis_manager.connect()

    async def on_shutdown():
        await redis_manager.disconnect()
        logger.info("Service stopped")


    await on_startup()
    yield
    await on_shutdown()



app = FastAPI(
    title=service_config.APP_NAME,
    version=service_config.APP_VERSION,
    lifespan=lifespan
)

register_exceptions_handlers(app)
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn_logger = logging.getLogger("uvicorn")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=service_config.DEBUG,
        log_config=None,
        log_level=uvicorn_logger.level
    )

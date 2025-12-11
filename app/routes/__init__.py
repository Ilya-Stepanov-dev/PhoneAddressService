from fastapi import APIRouter
from app.routes.routes import router

api_router = APIRouter(prefix="/api")
api_router.include_router(router)

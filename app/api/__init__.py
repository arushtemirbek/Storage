from fastapi import APIRouter
from app.api import health

router = APIRouter()

# Подключаем все модули API
router.include_router(health.router, prefix="/health", tags=["healthcheck"])

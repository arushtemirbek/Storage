from fastapi import FastAPI
from app.api import router as api_router
from app.settings.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# Подключаем роуты
app.include_router(api_router)

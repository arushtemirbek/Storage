from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from app.api import router as api_router
from app.settings.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
# Подключаем роуты
app.include_router(api_router)

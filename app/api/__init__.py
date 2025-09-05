from fastapi import APIRouter
from app.api import health, auth, files

router = APIRouter()


router.include_router(health.router, prefix="", tags=["healthcheck"])
router.include_router(auth.router, prefix="", tags=["auth"])
router.include_router(files.router, prefix="", tags=["files"])

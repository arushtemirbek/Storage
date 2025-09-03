from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def ping():
    return {"status": "ok"}

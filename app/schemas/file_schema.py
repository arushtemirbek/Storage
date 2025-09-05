from pydantic import BaseModel
from datetime import datetime
from app.models.models import VisibilityEnum


class FileOut(BaseModel):
    id: int
    filename: str
    size: int
    mimetype: str
    visibility: VisibilityEnum
    downloads_count: int
    created_at: datetime

    class Config:
        orm_mode = True

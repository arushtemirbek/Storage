import os
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.models import File as FileModel, VisibilityEnum
from app.schemas.file_schema import FileOut
from datetime import datetime
from uuid import uuid4

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload", response_model=FileOut)
async def upload_file(
    file: UploadFile = File(...),
    visibility: VisibilityEnum = Form(...),
    db: AsyncSession = Depends(get_db),
    current_user_id: int = 2,
    current_department_id: int = 1,
):
    ext = os.path.splitext(file.filename)[1]
    new_filename = f"{uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, new_filename)

    content = await file.read()
    size = len(content)

    if size > 100 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large")

    with open(file_path, "wb") as f:
        f.write(content)

    new_file = FileModel(
        filename=file.filename,
        path=file_path,
        size=size,
        mimetype=file.content_type,
        visibility=visibility,
        owner_id=current_user_id,
        department_id=current_department_id,
        created_at=datetime.utcnow(),
    )

    db.add(new_file)
    await db.commit()
    await db.refresh(new_file)

    # TODO: вызвать Celery задачу для извлечения метаданных

    return new_file

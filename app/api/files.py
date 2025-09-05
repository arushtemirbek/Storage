from fastapi import APIRouter, UploadFile, Depends, HTTPException, Form, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.minio_session import save_files
from app.database.session import get_db
from app.dependencies.check_token import get_current_user
from app.models import User, VisibilityEnum
from app.services.files import save_file_record, validate_file_upload

router = APIRouter()


@router.post("/upload")
async def upload_file(
    file: UploadFile,
    visibility: VisibilityEnum = Query(...),  # только видимость в query
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # проверяем файл по роли пользователя
    validate_file_upload(
        user_role=current_user.role,
        file=file,
        visibility=visibility,
    )

    file_path = await save_files(file)

    new_file = await save_file_record(
        db=db,
        filename=file.filename,
        path=file_path,
        mimetype=file.content_type,
        owner_id=current_user.id,
        department_id=current_user.department_id,  # <-- напрямую, без lazy load
        visibility=visibility,
    )

    return {"file_id": new_file.id, "path": new_file.path}

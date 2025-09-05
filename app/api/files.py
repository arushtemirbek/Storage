from fastapi import APIRouter, UploadFile, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from app.models import File, User
from app.database.minio_session import minio_client
from minio.error import S3Error
from io import BytesIO

from app.database.minio_session import save_files
from app.database.session import get_db
from app.dependencies.check_token import get_current_user
from app.models import User, VisibilityEnum
from app.services.files import save_file_record, validate_file_upload


router = APIRouter()


@router.post("/upload")
async def upload_file(
    file: UploadFile,
    visibility: VisibilityEnum = Query(...),
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


@router.get("/{file_id}/download")
async def download_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # ищем файл в БД
    result = await db.execute(select(File).where(File.id == file_id))
    file: File | None = result.scalar_one_or_none()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    # проверка доступа
    if current_user.role == "USER":
        if file.owner_id != current_user.id or file.visibility != "PRIVATE":
            raise HTTPException(status_code=403, detail="Access denied")

    elif current_user.role == "MANAGER":
        if (
            file.owner_id != current_user.id
            and file.department_id != current_user.department_id
        ):
            raise HTTPException(status_code=403, detail="Access denied")

    elif current_user.role == "ADMIN":
        pass  # всегда доступ разрешён

    else:
        raise HTTPException(status_code=403, detail="Unknown role")
    print(1111111111111111111111111111111111111111111111)
    # скачиваем файл из Minio
    try:
        response = minio_client.get_object("files", file.path)
        data = BytesIO(response.read())
        response.close()
        response.release_conn()
    except S3Error as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error fetching file from storage")

    return StreamingResponse(
        data,
        media_type=file.mimetype,
        headers={"Content-Disposition": f"attachment; filename={file.filename}"}
    )

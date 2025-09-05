from sqlalchemy.ext.asyncio import AsyncSession
from app.models import File, VisibilityEnum, RoleEnum
from fastapi import UploadFile, HTTPException


async def save_file_record(
    db: AsyncSession,
    filename: str,
    path: str,
    mimetype: str,
    owner_id: int,
    department_id: int,
    visibility: VisibilityEnum = VisibilityEnum.PRIVATE
) -> File:
    """Создаём запись о файле в БД"""

    new_file = File(
        filename=filename,
        path=path,
        size=0,
        mimetype=mimetype,
        visibility=visibility,
        owner_id=owner_id,
        department_id=department_id,
    )
    db.add(new_file)
    await db.commit()
    await db.refresh(new_file)
    return new_file


def validate_file_upload(user_role: RoleEnum, file: UploadFile, visibility: VisibilityEnum):
    if user_role == RoleEnum.USER:
        max_size = 10 * 1024 * 1024
        allowed_types = ["application/pdf"]
        allowed_visibility = [VisibilityEnum.PRIVATE]
    elif user_role == RoleEnum.MANAGER:
        max_size = 50 * 1024 * 1024
        allowed_types = ["application/pdf", "application/msword",
                         "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
        allowed_visibility = [VisibilityEnum.PRIVATE, VisibilityEnum.DEPARTMENT, VisibilityEnum.PUBLIC]
    elif user_role == RoleEnum.ADMIN:
        max_size = 100 * 1024 * 1024
        allowed_types = []  # любые
        allowed_visibility = [VisibilityEnum.PRIVATE, VisibilityEnum.DEPARTMENT, VisibilityEnum.PUBLIC]
    else:
        raise HTTPException(status_code=403, detail="Unknown role")
    if allowed_types and file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="File type not allowed")

    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)
    if size > max_size:
        raise HTTPException(status_code=400, detail="File too large")

    if visibility not in allowed_visibility:
        raise HTTPException(status_code=403, detail="Not allowed to use this visibility")

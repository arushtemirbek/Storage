from sqlalchemy.ext.asyncio import AsyncSession
from app.models import File, VisibilityEnum


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
        size=0,  # при желании можно вычислить
        mimetype=mimetype,
        visibility=visibility,
        owner_id=owner_id,
        department_id=department_id,
    )
    db.add(new_file)
    await db.commit()
    await db.refresh(new_file)
    return new_file

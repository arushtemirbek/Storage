from fastapi import APIRouter, UploadFile, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.minio_session import save_files
from app.database.session import get_db
from app.models import File, VisibilityEnum

router = APIRouter()


@router.post("/upload")
async def upload_file(
    file: UploadFile,
    db: AsyncSession = Depends(get_db),
    owner_id: int = 2,
    department_id: int = 1
):
    try:
        file_path = await save_files(file)

        # сохраняем запись в БД
        new_file = File(
            filename=file.filename,
            path=file_path,
            size=0,
            mimetype=file.content_type,
            visibility=VisibilityEnum.PRIVATE,
            owner_id=owner_id,
            department_id=department_id,
        )
        db.add(new_file)
        await db.commit()
        await db.refresh(new_file)

        return {"file_id": new_file.id, "path": new_file.path}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

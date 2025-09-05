from fastapi import APIRouter, UploadFile, Depends, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.minio_session import save_files
from app.database.session import get_db
from app.dependencies.check_token import get_current_user
from app.models import User
from app.services.files import save_file_record, validate_file_upload

router = APIRouter()


@router.post("/upload")
async def upload_file(
    file: UploadFile,
    current_user: User = Depends(get_current_user),
    deps: dict = Depends(validate_file_upload),
    db: AsyncSession = Depends(get_db)):
    try:
        file_path = await save_files(file)
        print(current_user.id)
        print(current_user.department)
        print(123)
        new_file = await save_file_record(
            db=db,
            filename=file.filename,
            path=file_path,
            mimetype=file.content_type,
            owner_id=current_user.id,
            department_id=current_user.department.id,
        )
        return {"file_id": new_file.id, "path": new_file.path}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

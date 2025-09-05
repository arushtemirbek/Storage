from fastapi import APIRouter, UploadFile, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from minio import Minio
from uuid import uuid4

from app.database.session import get_db
from app.models import File, VisibilityEnum

router = APIRouter()

# Настраиваем MinIO клиент
minio_client = Minio(
    "localhost:9000",  # если в докере вместе с API, то "minio:9000"
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

BUCKET_NAME = "files"

# Создаём bucket, если нет
if not minio_client.bucket_exists(BUCKET_NAME):
    minio_client.make_bucket(BUCKET_NAME)


@router.post("/upload")
async def upload_file(
    file: UploadFile,
    db: AsyncSession = Depends(get_db),
    owner_id: int = 1,  # пока захардкодим для теста
    department_id: int = 1
):
    try:
        # генерим уникальное имя
        file_id = str(uuid4())
        object_name = f"{file_id}_{file.filename}"

        # загружаем в MinIO
        minio_client.put_object(
            BUCKET_NAME,
            object_name,
            file.file,  # поток
            length=-1,  # не знаем длину, MinIO сам определит
            part_size=10 * 1024 * 1024,  # chunk 10MB
            content_type=file.content_type
        )

        # сохраняем запись в БД
        new_file = File(
            filename=file.filename,
            path=f"{BUCKET_NAME}/{object_name}",
            size=0,  # можно считать через file.spool_max_size
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

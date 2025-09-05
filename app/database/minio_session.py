from uuid import uuid4

from fastapi import HTTPException
from minio import Minio

from app.settings.config import settings


# Настраиваем MinIO клиент
minio_client = Minio(
    "localhost:9000",  # если в докере вместе с API, то "minio:9000"
    access_key=settings.MINIO_USERNAME,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False
)


async def save_files(file):
    BUCKET_NAME = f"files"

    # Создаём bucket, если нет
    if not minio_client.bucket_exists(BUCKET_NAME):
        minio_client.make_bucket(BUCKET_NAME)

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
        return object_name

    except Exception as e:
        raise HTTPException(status_code=500, detail="Some error when saving file in minio")

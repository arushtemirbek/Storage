# import os
# from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
# from app.database.session import get_db
# from app.models import File as FileModel, VisibilityEnum
# from app.schemas.file_schema import FileOut
# from datetime import datetime
# from uuid import uuid4
#
# async def create_file(db: AsyncSession, department_id: int, file: File) -> File:
#

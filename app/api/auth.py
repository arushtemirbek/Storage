from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.session import get_db
from app.schemas.user_schema import UserRegister, UserLogin, Token, UserOut
from app.services.user_service import get_user_by_username, create_user
from app.services.department import get_department_by_id
from app.settings.security import verify_password, create_access_token



router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut)
async def register(user_in: UserRegister, db: AsyncSession = Depends(get_db)):
    existing = await get_user_by_username(db, user_in.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    department = await get_department_by_id(db, user_in.department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    user = await create_user(
        db,
        username=user_in.username,
        password=user_in.password,
        role=user_in.role,
        department_id=user_in.department_id,
    )
    return user


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                db: AsyncSession = Depends(get_db)):
    user = await get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id), "role": user.role})
    return {"access_token": token, "token_type": "bearer"}

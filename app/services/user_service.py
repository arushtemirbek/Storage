from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import User
from app.settings.security import hash_password


async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, username: str, password: str, role, department_id: int) -> User:
    user = User(
        username=username,
        password_hash=hash_password(password),
        role=role,
        department_id=department_id,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Department


async def get_department_by_id(db: AsyncSession, department_id: int) -> Department | None:
    result = await db.execute(select(Department).where(Department.id == department_id))
    return result.scalar_one_or_none()

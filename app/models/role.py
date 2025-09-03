from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.models import Base


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"<Role(id={self.id}, name={self.name})>"

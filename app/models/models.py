from sqlalchemy import String, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import enum
from datetime import datetime


class Base(DeclarativeBase):
    pass


class RoleEnum(str, enum.Enum):
    USER = "USER"
    MANAGER = "MANAGER"
    ADMIN = "ADMIN"


class VisibilityEnum(str, enum.Enum):
    PRIVATE = "PRIVATE"
    DEPARTMENT = "DEPARTMENT"
    PUBLIC = "PUBLIC"


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    users: Mapped[list["User"]] = relationship(back_populates="department")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), nullable=False)

    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"), nullable=False)
    department: Mapped["Department"] = relationship(back_populates="users")

    files: Mapped[list["File"]] = relationship(back_populates="owner")


class File(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    path: Mapped[str] = mapped_column(String(500), nullable=False)  # путь в S3
    size: Mapped[int] = mapped_column(Integer, nullable=False)  # байты
    mimetype: Mapped[str] = mapped_column(String(100), nullable=False)

    visibility: Mapped[VisibilityEnum] = mapped_column(Enum(VisibilityEnum), nullable=False)

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    owner: Mapped["User"] = relationship(back_populates="files")

    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"), nullable=False)
    department: Mapped["Department"] = relationship()

    downloads_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class FileMetadata(Base):
    __tablename__ = "file_metadata"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    file_id: Mapped[int] = mapped_column(ForeignKey("files.id"), unique=True, nullable=False)
    file: Mapped["File"] = relationship()

    author: Mapped[str | None] = mapped_column(String(255))
    title: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime | None] = mapped_column(DateTime)

    pages: Mapped[int | None] = mapped_column(Integer)
    producer: Mapped[str | None] = mapped_column(String(255))  # программа создания

    paragraphs: Mapped[int | None] = mapped_column(Integer)
    tables: Mapped[int | None] = mapped_column(Integer)

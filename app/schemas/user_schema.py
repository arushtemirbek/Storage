from pydantic import BaseModel, constr
from app.models import RoleEnum


class UserRegister(BaseModel):
    username: constr(min_length=3, max_length=100)
    password: constr(min_length=6, max_length=100)
    role: RoleEnum = RoleEnum.USER
    department_id: int


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    username: str
    role: RoleEnum
    department_id: int

    class Config:
        orm_mode = True

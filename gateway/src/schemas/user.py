from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
    login: str
    password: str


class UserUpdate(UserBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[str] = None
    email: Optional[str] = None
    phone_num: Optional[str] = None


class User(UserCreate):
    id: int
    first_name: str
    last_name: str
    birth_date: str
    email: str
    phone_num: str

    class Config:
        from_attributes = True

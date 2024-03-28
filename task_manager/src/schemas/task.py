from typing import Optional
from pydantic import BaseModel


class TaskBase(BaseModel):
    pass


class TaskCreate(TaskBase):
    creator_login: str
    name: str
    text: str


class TaskUpdate(TaskBase):
    name: Optional[str] = None
    text: Optional[str] = None


class Task(TaskCreate):
    id: int

    class Config:
        from_attributes = True

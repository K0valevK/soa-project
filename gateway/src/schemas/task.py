from typing import Optional
from pydantic import BaseModel


class TaskBase(BaseModel):
    pass


class TaskCreate(TaskBase):
    name: str
    text: str


class TaskUpdate(TaskBase):
    new_name: Optional[str] = None
    text: Optional[str] = None


class Task(TaskCreate):
    creator_login: str
    id: int

    class Config:
        from_attributes = True

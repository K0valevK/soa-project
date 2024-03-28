from typing import Optional
from pydantic import BaseModel


class CommentBase(BaseModel):
    pass


class CommentCreate(CommentBase):
    task_id: int
    creator_login: str
    to_comment: int
    text: str


class Comment(CommentCreate):
    id: int

    class Config:
        from_attributes = True

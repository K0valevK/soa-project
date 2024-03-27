from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from schemas import Task as TaskSchema

from database import Base


class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    creator_login: Mapped[str] = mapped_column(String, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String)
    text: Mapped[str] = mapped_column(String)


def toTaskSchema(task: Task) -> TaskSchema:
    return TaskSchema(id=task.id,
                      creator_login=task.creator_login,
                      name=task.name,
                      text=task.text)

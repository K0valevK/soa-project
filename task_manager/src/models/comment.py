from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String

from database import Base


class Comment(Base):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    task_id: Mapped[int] = mapped_column(Integer, nullable=False)
    creator_login: Mapped[str] = mapped_column(String, nullable=False, index=True)
    to_comment: Mapped[int] = mapped_column(Integer, nullable=False)
    text: Mapped[str] = mapped_column(String)

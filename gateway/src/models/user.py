from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String

from . import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    login: Mapped[str] = mapped_column(String, index=True, unique=True)
    password: Mapped[str] = mapped_column(String)
    first_name: Mapped[str] = mapped_column(String, default="")
    last_name: Mapped[str] = mapped_column(String, default="")
    birth_date: Mapped[str] = mapped_column(String, default="")
    email: Mapped[str] = mapped_column(String, default="")
    phone_num: Mapped[str] = mapped_column(String, default="")

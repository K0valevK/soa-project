from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from schemas import User as UserSchema

from database import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    login: Mapped[str] = mapped_column(String, unique=True, index=True)


def toUserSchema(user: User):
    return UserSchema(id=user.id,
                      login=user.login)

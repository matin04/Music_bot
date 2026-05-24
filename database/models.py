from sqlalchemy import (
    BigInteger,
    String,
    Integer
)

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from database.database import Base


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True
    )


class Download(Base):

    __tablename__ = "downloads"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger
    )

    query: Mapped[str] = mapped_column(
        String
    )
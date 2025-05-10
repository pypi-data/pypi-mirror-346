from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from kupala.authentication import BaseUser
from kupala.database.models import Base


class User(BaseUser):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str] = mapped_column(default="__password_hash__")
    profile: Mapped[Profile] = relationship("Profile", back_populates="user")
    scopes: Mapped[list[str]] = mapped_column(sa.JSON, default=list)

    @property
    def identity(self) -> str:
        return self.email

    def get_scopes(self) -> list[str]:
        return self.scopes


class Profile(Base):
    __tablename__ = "profiles"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id"))
    bio: Mapped[str]
    user: Mapped[User] = relationship("User", back_populates="profile")

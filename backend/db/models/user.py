from sqlalchemy.orm import Mapped, mapped_column
from db.models.base import Base

class User(Base):

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(default=False)
from enum import Enum
import datetime

from sqlalchemy import String, Integer, CheckConstraint, DateTime, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from db.models.base import Base

class TicketStatus(str, Enum):
    NEW = 'new'
    IN_PROGRESS = 'in_progress'
    DONE = 'done'

class TicketPriority(str, Enum):
    LOW = 'low'
    NORMAL = 'normal'
    HIGH = 'high'

class Ticket(Base):
    __table_args__ = (
        CheckConstraint("length(title) >= 3 AND length(title) <= 120"),
        CheckConstraint("description IS NULL OR length(description) <= 1000"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    title: Mapped[str] = mapped_column(String(120), nullable=False)

    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    status: Mapped[TicketStatus] = mapped_column(
        SQLEnum(
            TicketStatus,
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
            validate_strings=True
        ),
        nullable=False,
        default=TicketStatus.NEW
    )

    priority: Mapped[TicketPriority] = mapped_column(
        SQLEnum(
            TicketPriority,
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
            validate_strings=True
        ),
        nullable=False,
        default=TicketPriority.LOW
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

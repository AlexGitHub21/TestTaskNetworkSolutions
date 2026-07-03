import datetime
from pydantic import BaseModel, ConfigDict
from enum import Enum

class TicketStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class TicketPriority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"

class BaseTicket(BaseModel):
    id: int
    title: str
    description: str | None = None
    status: TicketStatus
    priority: TicketPriority

    model_config = ConfigDict(from_attributes=True)

class TicketCreate(BaseModel):
    title: str
    description: str | None = None
    priority: TicketPriority

    model_config = ConfigDict(from_attributes=True)

class TicketUpdate(BaseModel):
    id: int
    status: TicketStatus

    model_config = ConfigDict(from_attributes=True)

class TicketResponse(BaseTicket):
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True
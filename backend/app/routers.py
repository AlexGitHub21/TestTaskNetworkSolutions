from fastapi import APIRouter, Depends, Query, Body
from starlette import status
from app.service import TicketService
from app.depends import get_current_admin
from db.models.user import User

from app.schemas import TicketCreate, BaseTicket, TicketResponse

ticket_router = APIRouter(prefix="/tickets", tags=["ticket"])


@ticket_router.post(
    path="/create_ticket",
    status_code=status.HTTP_201_CREATED)
async def create_ticket(ticket: TicketCreate, service: TicketService = Depends(TicketService)) -> TicketCreate:
    return await service.create_ticket(ticket)


@ticket_router.get(
    path="",
    response_model=list[TicketResponse],
    status_code=status.HTTP_200_OK
)
async def get_all_tickets(
        limit: int = Query(10, ge=1, le=100),
        offset: int = Query(0, ge=0),
        status: str | None = None,
        priority: str | None = None,
        search: str | None = None,
        sort_by: str  | None = None,
        order: str | None = None,
        service: TicketService = Depends(TicketService)) -> list[TicketResponse]:
    return await service.get_all_tickets(
        limit=limit,
        offset=offset,
        status=status,
        priority=priority,
        search=search,
        sort_by=sort_by,
        order=order,
    )

@ticket_router.patch(
    path="/{ticket_id}/status",
    status_code=status.HTTP_200_OK,
)
async def update_status_ticket(ticket_id: int, status_ticket: str = Body(...), service: TicketService = Depends(TicketService)):
    return await service.update_status(ticket_id, status_ticket)


@ticket_router.delete(
    path="/{ticket_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_ticket(ticket_id: int,
                        _: User = Depends(get_current_admin),
                        service: TicketService = Depends(TicketService)):
    return await service.delete_ticket(ticket_id)


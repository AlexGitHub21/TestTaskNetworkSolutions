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
#
# @ticket_router.get(
#     path="/priority/{priority}",
#     response_model=list[BaseTicket],
#     status_code=status.HTTP_200_OK
# )
# async def get_tickets_by_priority(priority: str, service: TicketService = Depends(TicketService)) -> list[BaseTicket]:
#     return await service.get_tickets_by_priority(priority=priority)
#
# @ticket_router.get(
#     path="/status/{status}",
#     response_model=list[BaseTicket],
#     status_code=status.HTTP_200_OK
# )
# async def get_tickets_by_status(status_ticket: str, service: TicketService = Depends(TicketService)) -> list[BaseTicket]:
#     return await service.get_tickets_by_status(status_ticket)


# @ticket_router.get(
#     path="/desc/{description}",
#     response_model=BaseTicket
# )
# async def get_ticket_by_description(description: str, service: TicketService = Depends(TicketService)):
#     return await service.get_tickets_by_desc(description)
#
#
# @ticket_router.get(
#     path="/title/{title}",
#     response_model=BaseTicket
# )
# async def get_ticket_by_title(title: str, service: TicketService = Depends(TicketService)):
#     return await service.get_tickets_by_title(title)

@ticket_router.get(
    path="/sorted_tickets",
    response_model=list[TicketResponse]
)
async def get_sorted_tickets(sort_by: str = "created_at", order: str = "asc", service: TicketService = Depends(TicketService)):
    return await service.get_sorted_tickets(sort_by=sort_by, order=order)

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


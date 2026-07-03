from fastapi import Depends, HTTPException
from app.managers import TicketManager
from app.schemas import TicketCreate, BaseTicket, TicketResponse, TicketStatus, TicketUpdate
from starlette import status


class TicketService:
    def __init__(self, manager: TicketManager = Depends(TicketManager)) -> None:
        self.manager = manager

    async def create_ticket(self, ticket: TicketCreate) -> TicketCreate:
        return await self.manager.create_ticket(ticket)

    async def get_all_tickets(
            self,
            limit: int,
            offset: int,
            status: str | None,
            priority: str | None,
            search: str | None,
            sort_by: str | None,
            order: str | None,
        ) -> list[TicketResponse]:
        return await self.manager.get_all_tickets(
            limit,
            offset,
            status,
            priority,
            search,
            sort_by,
            order,)

    # async def get_tickets_by_priority(self, priority: str) -> list[BaseTicket]:
    #     return await self.manager.get_tickets_by_priority(priority)
    #
    # async def get_tickets_by_status(self, status_ticket: str) -> list[BaseTicket]:
    #     return await self.manager.get_tickets_by_status(status_ticket)

    # async def get_tickets_by_desc(self, desc: str) -> BaseTicket:
    #     ticket = await self.manager.get_tickets_by_desc(desc)
    #
    #     if ticket is None:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail=f"Не найдена заявка с таким описанием: {desc}",
    #         )
    #     return BaseTicket.model_validate(ticket)
    #
    # async def get_tickets_by_title(self, title: str) -> BaseTicket:
    #     ticket = await self.manager.get_tickets_by_title(title)
    #
    #     if ticket is None:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail=f"Не найдена заявка с таким заголовком: {title}",
    #         )
    #     return BaseTicket.model_validate(ticket)

    async def get_sorted_tickets(self, sort_by: str, order: str) -> list[TicketResponse]:

        if order not in ("asc", "desc"):
            raise HTTPException(
                status_code=400,
                detail="Параметр order должен быть 'asc' или 'desc'"
            )
        if sort_by not in ("created_at", "priority"):
            raise HTTPException(
                status_code=400,
                detail="Параметр sort_by должен быть 'created_at' или 'priority'"
            )
        return await self.manager.get_all_sorted_tickets(sort_by, order)


    async def update_status(self, ticket_id: int, status_ticket: str) -> TicketUpdate:
        ticket = await self.manager.get_ticket(ticket_id)
        if ticket is None:
            raise HTTPException(
                status_code=404,
                detail="Заявка не найдена"
            )
        if ticket.status == TicketStatus.DONE:
            raise HTTPException(
                status_code=400,
                detail="Нельзя заменить статус завершенной заявки"
            )
        if status_ticket not in ("in_progress", "done"):
            raise HTTPException(
                status_code=400,
                detail="Параметр status_ticket должен быть 'in_progress' или 'done'"
            )
        await self.manager.update_ticket(ticket_id, status_ticket)
        return TicketUpdate.model_validate({"id": ticket_id, "status": status_ticket})

    async def delete_ticket(self, ticket_id: int) -> None:
        ticket = await self.manager.get_ticket(ticket_id)
        if ticket.status == TicketStatus.DONE:
            raise HTTPException(
                status_code=400,
                detail="Нельзя удалить заявку в статусе done"
            )
        if ticket is None:
            raise HTTPException(
                status_code=404,
                detail="Заявка с таким id не найдена"
            )
        return await self.manager.delete_ticket(ticket_id)
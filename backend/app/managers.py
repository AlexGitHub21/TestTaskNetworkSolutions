from app.schemas import TicketCreate, BaseTicket, TicketPriority, TicketResponse, TicketUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_session
from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import update, select, delete, case, desc, asc, or_

from db.models import Ticket


class TicketManager:
    def __init__(self, db_session: AsyncSession = Depends(get_session)):
        self.model = Ticket
        self.db_session = db_session

    async def create_ticket(self, ticket: TicketCreate) -> TicketCreate:
        new_note = self.model(**ticket.model_dump())
        self.db_session.add(new_note)
        try:
            await self.db_session.commit()
            await self.db_session.refresh(new_note)  # синхронизируем объект с БД
        except IntegrityError:
            await self.db_session.rollback()
            raise

        return TicketCreate.model_validate(new_note)

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
        query = select(self.model)
        if status:
            query = query.where(self.model.status == status)
        if priority:
            query = query.where(self.model.priority == priority)
        if search:
            query = query.where(
                or_(
                    self.model.title.ilike(f"%{search}%"),
                    self.model.description.ilike(f"%{search}%"),
                )
            )
        if sort_by:
            if sort_by == "created_at":
                column = self.model.created_at
            elif sort_by == "priority":
                column = case(
                    (self.model.priority == TicketPriority.LOW, 1),
                    (self.model.priority == TicketPriority.NORMAL, 2),
                    (self.model.priority == TicketPriority.HIGH, 3),
                )
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Некорректное поле сортировки",
                )

            if order == "desc":
                query = query.order_by(desc(column))

            else:
                query = query.order_by(asc(column))

        query = query.limit(limit).offset(offset)

        result = await self.db_session.execute(query)
        tickets = result.scalars().all()

        return [TicketResponse.model_validate(ticket) for ticket in tickets]

    # async def get_tickets_by_priority(self, priority: str) -> list[BaseTicket]:
    #     query = select(self.model).where(self.model.priority == priority)
    #
    #     result = await self.db_session.execute(query)
    #     tickets = result.scalars().all()
    #
    #     return [BaseTicket.model_validate(ticket) for ticket in tickets]
    #
    # async def get_tickets_by_status(self, status: str) -> list[BaseTicket]:
    #     query = select(self.model).where(self.model.status == status)
    #
    #     result = await self.db_session.execute(query)
    #     tickets = result.scalars().all()
    #
    #     return [BaseTicket.model_validate(ticket) for ticket in tickets]

    # async def get_tickets_by_desc(self, desc: str) -> BaseTicket:
    #     query = select(self.model).where(self.model.description == desc)
    #
    #     result = await self.db_session.execute(query)
    #     ticket = result.scalars().one_or_none()
    #     return ticket
    #
    # async def get_tickets_by_title(self, title: str) -> BaseTicket:
    #     query = select(self.model).where(self.model.title == title)
    #
    #     result = await self.db_session.execute(query)
    #     ticket = result.scalars().one_or_none()
    #     return ticket


    # async def get_all_sorted_tickets(self, sort_by: str, order: str) -> list[TicketResponse]:
    #
    #     query = select(self.model)
    #
    #     if sort_by == "created_at":
    #         column = self.model.created_at
    #     elif sort_by == "priority":
    #         column = case(
    #             (self.model.priority == TicketPriority.LOW, 1),
    #             (self.model.priority == TicketPriority.NORMAL, 2),
    #             (self.model.priority == TicketPriority.HIGH, 3),
    #         )
    #     else:
    #         raise ValueError("Invalid sort field")
    #
    #     if order == "desc":
    #         query = query.order_by(desc(column))
    #
    #     else:
    #         query = query.order_by(asc(column))
    #
    #     result = await self.db_session.execute(query)
    #     tickets = result.scalars().all()
    #     return [TicketResponse.model_validate(ticket) for ticket in tickets]

    async def get_ticket(self, ticket_id: int) -> TicketUpdate:
        query = select(self.model).where(self.model.id == ticket_id)

        result = await self.db_session.execute(query)
        ticket = result.scalars().one_or_none()
        return ticket

    async def update_ticket(self, ticket_id, status_ticket: str) -> None:
        query = (
            update(self.model)
            .where(
                self.model.id == ticket_id)
            .values(status = status_ticket)
        )
        try:
            await self.db_session.execute(query)
            await self.db_session.commit()
        except SQLAlchemyError:
            await self.db_session.rollback()
            raise

    async def delete_ticket(self, ticket_id: int) -> None:
        query = (
            delete(self.model)
            .where(self.model.id == ticket_id)
        )

        try:
            await self.db_session.execute(query)
            await self.db_session.commit()

        except SQLAlchemyError:
            await self.db_session.rollback()
            raise
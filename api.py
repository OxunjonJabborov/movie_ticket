from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from schemes import TicketCreate, TicketOut, TicketGet
from database import Base, get_db, engine
from models import Ticket


Base.metadata.create_all(bind=engine)

api_router = APIRouter(prefix="/api/tickets")


@api_router.post("/", response_model=TicketOut)
def create_ticket(ticket_in: TicketCreate, db = Depends(get_db)):
    stmt = select(Ticket).where(Ticket.movie_name == ticket_in.movie_name,
                                Ticket.seat_number == ticket_in.seat_number)
    exicting_ticket = db.scalar(stmt)
    if exicting_ticket:
        raise HTTPException(status_code=404, detail="Bu bilet allaqachon sotilgan.")

    price = 80000 if ticket_in.is_vip else 40000

    ticket = Ticket(
        **ticket_in.model_dump(),
        price = price
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket

@api_router.get("/", response_model=list[TicketGet])
def get_tickets(db = Depends(get_db)):
    stmt = select(Ticket)
    tickets = db.scalars(stmt).all()
    return tickets

# @api_router.get("/tickets/{seat_number}", response_model=TicketGet)
# def find_seat_number(seat_number: int):
#     for ticket in tickets:
#         if ticket["seat_number"] == seat_number:
#             return ticket
#     raise HTTPException(status_code=404,detail="Bunday chipta topilmadi")

# @api_router.get("/tickets/{movie_name}", response_model=TicketGet)
# def find_movie_name(movie_name: str):
#     for ticket in tickets:
#         if ticket["movie_name"] == movie_name:
#             return ticket
#     raise HTTPException(status_code=404, detail="Bunday kino topilmadi")

# @api_router.delete("/")
# def delete_ticket(ticket: TicketCreate):
#     for del_ticket in tickets:
#         if (del_ticket["seat_number"] == ticket.seat_number and 
#             del_ticket["movie_name"] == ticket.movie_name):
#             tickets.remove(del_ticket)
#             return "message:" f"{del_ticket} o'chirildi"

#     raise HTTPException(status_code=404, detail="Ushbu chipta topilmadi")
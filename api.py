from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from schemas import TicketCreate, TicketOut, TicketGet
from database import Base, get_db, engine
from models import Ticket


Base.metadata.create_all(bind=engine)

api_router = APIRouter(prefix="/api/tickets")

VIP_PRICE = 80000
REGULAR_PRICE = 40000


@api_router.post("/", response_model=TicketOut)
def create_ticket(ticket_in: TicketCreate, db: Session = Depends(get_db)):
    stmt = select(Ticket).where(Ticket.movie_name == ticket_in.movie_name,
                                Ticket.seat_number == ticket_in.seat_number)
    existing_ticket = db.scalar(stmt)
    if existing_ticket:
        raise HTTPException(status_code=404, detail="Bu bilet allaqachon sotilgan.")

    price = VIP_PRICE if ticket_in.is_vip else REGULAR_PRICE

    ticket = Ticket(
        **ticket_in.model_dump(),
        price=price,
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


@api_router.get("/", response_model=list[TicketGet])
def get_tickets(db: Session = Depends(get_db)):
    stmt = select(Ticket)
    tickets = db.scalars(stmt).all()
    return tickets


@api_router.get("/tickets/{seat_number}", response_model=list[TicketGet])
def find_seat_number(seat_number: int, db: Session = Depends(get_db)):
    stmt = select(Ticket).where(Ticket.seat_number == seat_number)
    tickets = db.scalars(stmt).all()
    if not tickets:
        raise HTTPException(status_code=404, detail="Bunday chipta topilmadi")
    return tickets


@api_router.get("/tickets/{movie_name}", response_model=list[TicketGet])
def find_movie_name(movie_name: str, db: Session = Depends(get_db)):
    stmt = select(Ticket).where(Ticket.movie_name == movie_name)
    tickets = db.scalars(stmt).all()
    if not tickets:
        raise HTTPException(status_code=404, detail="Bunday kino topilmadi")
    return tickets


@api_router.delete("/")
def delete_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    stmt = select(Ticket).where(Ticket.movie_name == ticket.movie_name,
                                Ticket.seat_number == ticket.seat_number)
    db.scalar(stmt)

    raise HTTPException(status_code=404, detail="Ushbu chipta topilmadi")

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from schemas import TicketCreate, TicketOut
from database import get_db
from models import Ticket

api_router = APIRouter(prefix="/api/tickets")

VIP_PRICE = 80000
REGULAR_PRICE = 40000


def calculate_price(is_vip: bool) -> int:
    return VIP_PRICE if is_vip else REGULAR_PRICE


def find_ticket(db: Session, movie_name: str, seat_number: int) -> Ticket | None:
    stmt = select(Ticket).where(Ticket.movie_name == movie_name,
                                Ticket.seat_number == seat_number)
    return db.scalar(stmt)


def find_tickets_or_404(db: Session, condition, not_found_detail: str) -> list[Ticket]:
    tickets = db.scalars(select(Ticket).where(condition)).all()
    if not tickets:
        raise HTTPException(status_code=404, detail=not_found_detail)
    return tickets


@api_router.post("/", response_model=TicketOut)
def create_ticket(ticket_in: TicketCreate, db: Session = Depends(get_db)):
    if find_ticket(db, ticket_in.movie_name, ticket_in.seat_number):
        raise HTTPException(status_code=404, detail="Bu bilet allaqachon sotilgan.")

    ticket = Ticket(
        **ticket_in.model_dump(),
        price=calculate_price(ticket_in.is_vip),
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


@api_router.get("/", response_model=list[TicketOut])
def get_tickets(db: Session = Depends(get_db)):
    return db.scalars(select(Ticket)).all()


@api_router.get("/tickets/{seat_number}", response_model=list[TicketOut])
def find_seat_number(seat_number: int, db: Session = Depends(get_db)):
    return find_tickets_or_404(db, Ticket.seat_number == seat_number,
                               "Bunday chipta topilmadi")


@api_router.get("/tickets/{movie_name}", response_model=list[TicketOut])
def find_movie_name(movie_name: str, db: Session = Depends(get_db)):
    return find_tickets_or_404(db, Ticket.movie_name == movie_name,
                               "Bunday kino topilmadi")


@api_router.delete("/")
def delete_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    find_ticket(db, ticket.movie_name, ticket.seat_number)

    raise HTTPException(status_code=404, detail="Ushbu chipta topilmadi")

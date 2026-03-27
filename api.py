from fastapi import APIRouter, HTTPException


from schemes import TicketCreate, TicketOut, TicketGet

api_router = APIRouter(prefix="/api/tickets")

tickets = []
current_ticket_id = 1

@api_router.post("/", response_model=TicketOut)
def create_ticket(ticket_in: TicketCreate):
    global current_ticket_id
    
    for sold_ticket in tickets:
        if (sold_ticket["seat_number"] == ticket_in.seat_number and 
            sold_ticket["movie_name"] == ticket_in.movie_name):
            raise HTTPException(status_code=404, detail="Bu bilet allaqachon sotilgan.")

    price = 80000 if ticket_in.is_vip else 40000

    new_ticket = {
        "ticket_id": current_ticket_id,
        "customer_name": ticket_in.customer_name,
        "seat_number": ticket_in.seat_number,
        "movie_name": ticket_in.movie_name,
        "is_vip": ticket_in.is_vip,
        "price": price,
        "status": ticket_in.status
    }
    tickets.append(new_ticket)
    current_ticket_id += 1
    
    return new_ticket

@api_router.get("/", response_model=list[TicketGet])
def get_ticket():
    return tickets

@api_router.get("/tickets/{seat_number}", response_model=TicketGet)
def find_seat_number(seat_number: int):
    for ticket in tickets:
        if ticket["seat_number"] == seat_number:
            return ticket
    raise HTTPException(status_code=404,detail="Bunday chipta topilmadi")

@api_router.get("/tickets/{movie_name}", response_model=TicketGet)
def find_movie_name(movie_name: str):
    for ticket in tickets:
        if ticket["movie_name"] == movie_name:
            return ticket
    raise HTTPException(status_code=404, detail="Bunday kino topilmadi")

@api_router.delete("/")
def delete_ticket(ticket: TicketCreate):
    for del_ticket in tickets:
        if (del_ticket["seat_number"] == ticket.seat_number and 
            del_ticket["movie_name"] == ticket.movie_name):
            tickets.remove(del_ticket)
            return "message:" f"{del_ticket} o'chirildi"

    raise HTTPException(status_code=404, detail="Ushbu chipta topilmadi")
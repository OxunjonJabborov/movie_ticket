from pydantic import BaseModel, Field

class TicketCreate(BaseModel):
    movie_name: str = Field(max_length=200, description="The name of the movie")
    seat_number: int = Field(ge=1, le=50)
    customer_name: str = Field(max_length=100, description="The name of the customer")
    is_vip: bool = False


class TicketOut(BaseModel):
    ticket_id: int = Field(ge=1)
    movie_name: str = Field(max_length=200)
    seat_number: int = Field(ge=1, le=50)
    customer_name: str = Field(max_length=100)
    is_vip: bool = False
    price: float = Field(default=0)


class TicketGet(BaseModel):
    ticket_id: int = Field()
    movie_name: str = Field()
    seat_number: int = Field()
    customer_name: str = Field()
    is_vip: bool = Field()
    price: float = Field()
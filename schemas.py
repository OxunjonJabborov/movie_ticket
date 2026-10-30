from pydantic import BaseModel, Field


class TicketBase(BaseModel):
    movie_name: str = Field(max_length=200, description="The name of the movie")
    seat_number: int = Field(ge=1, le=50)
    customer_name: str = Field(max_length=100, description="The name of the customer")
    is_vip: bool = False
    status: str = Field(description="Chipta holati, masalan: band")


class TicketCreate(TicketBase):
    pass


class TicketDelete(BaseModel):
    movie_name: str
    seat_number: int


class TicketOut(TicketBase):
    id: int
    price: float

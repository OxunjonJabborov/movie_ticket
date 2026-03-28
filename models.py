from sqlalchemy import String, Integer, Numeric, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column
from database import Base, engine

Base.metadata.create_all(bind=engine)

class Ticket(Base):
    __tablename__='tickets'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    movie_name: Mapped[str] = mapped_column(String(length=100))
    customer_name: Mapped[str] = mapped_column(String(length=100))
    seat_number: Mapped[int] = mapped_column(Integer, nullable=False)
    is_vip: Mapped[bool] = mapped_column(Boolean, default=False)
    price: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String)
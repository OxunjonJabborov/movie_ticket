import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app

TICKET = {"movie_name": "Avatar", "seat_number": 5,
          "customer_name": "Ali", "status": "band"}


@pytest.fixture
def client():
    engine = create_engine("sqlite://",
                           connect_args={"check_same_thread": False},
                           poolclass=StaticPool)
    Base.metadata.create_all(bind=engine)
    TestSession = sessionmaker(bind=engine, autoflush=False)

    def override_get_db():
        db = TestSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_create_ticket_regular_price(client):
    response = client.post("/api/tickets/", json=TICKET)
    assert response.status_code == 200
    assert response.json() == {**TICKET, "id": 1, "is_vip": False, "price": 40000}


def test_create_ticket_vip_price(client):
    response = client.post("/api/tickets/", json={**TICKET, "is_vip": True})
    assert response.status_code == 200
    assert response.json()["price"] == 80000


def test_create_duplicate_ticket_is_rejected(client):
    client.post("/api/tickets/", json=TICKET)
    response = client.post("/api/tickets/", json=TICKET)
    assert response.status_code == 409
    assert response.json() == {"detail": "Bu bilet allaqachon sotilgan."}


def test_create_ticket_validates_seat_number(client):
    response = client.post("/api/tickets/", json={**TICKET, "seat_number": 51})
    assert response.status_code == 422


def test_get_tickets(client):
    assert client.get("/api/tickets/").json() == []
    client.post("/api/tickets/", json=TICKET)
    tickets = client.get("/api/tickets/").json()
    assert [t["seat_number"] for t in tickets] == [5]


def test_find_by_seat_number(client):
    client.post("/api/tickets/", json=TICKET)
    response = client.get("/api/tickets/tickets/5")
    assert response.status_code == 200
    assert response.json()[0]["movie_name"] == "Avatar"


def test_find_by_seat_number_not_found(client):
    response = client.get("/api/tickets/tickets/7")
    assert response.status_code == 404
    assert response.json() == {"detail": "Bunday chipta topilmadi"}


def test_find_by_movie_name(client):
    client.post("/api/tickets/", json=TICKET)
    response = client.get("/api/tickets/movie/Avatar")
    assert response.status_code == 200
    assert response.json()[0]["seat_number"] == 5


def test_find_by_movie_name_not_found(client):
    response = client.get("/api/tickets/movie/Titanic")
    assert response.status_code == 404
    assert response.json() == {"detail": "Bunday kino topilmadi"}


def test_delete_ticket_never_deletes(client):
    client.post("/api/tickets/", json=TICKET)
    response = client.request("DELETE", "/api/tickets/", json=TICKET)
    assert response.status_code == 404
    assert response.json() == {"detail": "Ushbu chipta topilmadi"}
    assert len(client.get("/api/tickets/").json()) == 1

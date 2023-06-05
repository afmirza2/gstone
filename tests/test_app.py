import os
os.environ['PROJECT_NAME'] = 'LoanAmoritization'
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.services import loan_service
from app.schemas.loan import LoanCreate
from app.main import app
from app.db.models import Base
from app.db.sqldb import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        
@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_user(test_db):    
    response = client.post("/users", json={"id": "greystone", "loans": []})
    
    assert response.status_code == 200
    assert response.json() == {"id": "greystone", "loans": []}
    
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json()[0]['id'] == "greystone"
    assert response.json()[0]['loans'] == []
    
def test_create_loan(test_db):
    client.post("/users", json={"id": "greystone"})
    response = client.post("/users/greystone/loans", json={
        "amount": 100000,
        "annual_interest_rate": 6.5,
        "loan_term_in_months": 12
    })
    assert response.status_code == 200
    
    data = response.json()
    assert data["amount"] == 100000.0
    assert data["annual_interest_rate"] == 6.5
    assert data["loan_term_in_months"] == 12
    assert data["id"]
    
    response = client.get("/users/greystone/loans")
    data = response.json()
    assert len(data) > 0
    
def test_loan_schedule(test_db):
    client.post("/users", json={"id": "greystone"})
    response = client.post("/users/greystone/loans", json={
        "amount": 100000,
        "annual_interest_rate": 6.5,
        "loan_term_in_months": 12
    })
    data = response.json()
    loan_id = data['id']
        
    response = client.get(f'/loans/{loan_id}/schedule')
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 12

def test_loan_amortization_schedule():
    amount = 50000
    loan_term_in_months = 12
    annual_interest_rate = 5.0
    loan = LoanCreate(loan_term_in_months=loan_term_in_months,
                      amount=amount, annual_interest_rate=annual_interest_rate)
    schedule = loan_service.amortization_schedule(
        loan
    )
    assert len(schedule) == loan_term_in_months
    for month in schedule:
        assert "month" in month
        assert "remaining_balance" in month
        assert "monthly_payment" in month

    assert schedule[0]['month'] == 1
    assert schedule[0]['remaining_balance'] == '45927.96'
    assert schedule[0]['monthly_payment'] == '4280.37'

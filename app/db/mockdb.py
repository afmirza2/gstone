from app.models.user import User
from app.models.loan import Loan

users = {}

users["jack"] = User(id="jack", loans=[Loan(
    amount=1000, annual_interest_rate=10, loan_term_in_months=12, id='1')])

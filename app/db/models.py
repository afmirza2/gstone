from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    loans = relationship("Loan", back_populates="user")


class Loan(Base):
    __tablename__ = "loans"

    id = Column(String, primary_key=True)
    amount = Column(Float)
    annual_interest_rate = Column(Float)
    loan_term_in_months = Column(Integer)
    user_id = Column(String, ForeignKey("users.id"))

    user = relationship("User", back_populates="loans")

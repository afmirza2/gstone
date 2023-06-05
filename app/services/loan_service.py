from app.schemas.loan import Loan


def amortization_schedule(loan: Loan):
    monthly_interest_rate = loan.annual_interest_rate / 12 / 100
    denominator = 1 - (1 + monthly_interest_rate) ** -loan.loan_term_in_months
    monthly_payment = loan.amount * (monthly_interest_rate / denominator)

    schedule = []
    balance = loan.amount
    for month in range(1, loan.loan_term_in_months + 1):
        interest = balance * monthly_interest_rate
        principal = monthly_payment - interest
        balance -= principal
        schedule.append({"month": month, "remaining_balance": '%.2f' % round(balance, 2),
                        "monthly_payment": '%.2f' % round(monthly_payment, 2)})
    return schedule

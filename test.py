from db import SessionLocal
from models import User, Category, Expense

with SessionLocal() as session:
    users = session.query(User).all()
    print("Users:", users)

    expenses = session.query(Expense).all()
    for e in expenses:
        print(e.id, e.name, e.amount, e.user_id, e.category_id)

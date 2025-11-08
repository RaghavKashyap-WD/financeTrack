from decimal import Decimal
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import SessionLocal
from models import User, Category, Expense
from sqlalchemy.orm import relationship, sessionmaker, declarative_base, joinedload

# ---------- USER ----------
def create_user(username, email=None):
    with SessionLocal() as s:
        u = User(username=username.strip(), email=(email.strip() if email else None))
        s.add(u)
        try:
            s.commit()
            s.refresh(u)
            return u
        except IntegrityError:
            s.rollback()
            raise ValueError("Username already exists.")
        except SQLAlchemyError:
            s.rollback()
            raise

def list_users():
    with SessionLocal() as s:
        return s.query(User).order_by(User.id).all()

# ---------- CATEGORY ----------
def create_category(name):
    with SessionLocal() as s:
        c = Category(name=name.strip())
        s.add(c)
        try:
            s.commit()
            s.refresh(c)
            return c
        except IntegrityError:
            s.rollback()
            raise ValueError("Category already exists.")
        except SQLAlchemyError:
            s.rollback()
            raise

def list_categories():
    with SessionLocal() as s:
        return s.query(Category).order_by(Category.id).all()

# ---------- EXPENSE ----------
def create_expense(user_id, category_id, name, amount):
    with SessionLocal() as s:
        e = Expense(user_id=user_id, category_id=category_id, name=name.strip(), amount=Decimal(str(amount)))
        s.add(e)
        try:
            s.commit()
            s.refresh(e)
            return e
        except SQLAlchemyError:
            s.rollback()
            raise

def list_expenses(user_id=None):
    """Return expenses with user and category eagerly loaded so they are usable after session closes."""
    with SessionLocal() as s:
        q = s.query(Expense).options(
            joinedload(Expense.user),
            joinedload(Expense.category)
        )
        if user_id:
            q = q.filter(Expense.user_id == user_id)
        return q.order_by(Expense.created_at.desc()).all()

def update_expense(expense_id, **fields):
    with SessionLocal() as s:
        e = s.get(Expense, expense_id)
        if not e:
            raise ValueError("Expense not found.")
        for k, v in fields.items():
            if hasattr(e, k):
                setattr(e, k, v)
        try:
            s.commit()
            s.refresh(e)
            return e
        except SQLAlchemyError:
            s.rollback()
            raise

def delete_expense(expense_id):
    with SessionLocal() as s:
        e = s.get(Expense, expense_id)
        if not e:
            raise ValueError("Expense not found.")
        try:
            s.delete(e)
            s.commit()
        except SQLAlchemyError:
            s.rollback()
            raise

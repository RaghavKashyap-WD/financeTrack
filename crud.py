from decimal import Decimal
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import SessionLocal
from models import User, Category, Expense
from sqlalchemy.orm import joinedload
from passlib.hash import bcrypt
from datetime import datetime, timedelta
from sqlalchemy import func

# ---------- USER ----------
def create_user(username, password, email=None):
    """Create user with password hashed."""
    with SessionLocal() as s:
        hashed = bcrypt.hash(password)
        u = User(username=username.strip(), email=(email.strip() if email else None), password_hash=hashed)
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

def authenticate_user(identifier, password):
    """identifier can be username or email. Returns user on success, None otherwise."""
    with SessionLocal() as s:
        q = s.query(User)
        if "@" in identifier:
            u = q.filter(User.email == identifier.strip()).first()
        else:
            u = q.filter(User.username == identifier.strip()).first()
        if not u:
            return None
        if bcrypt.verify(password, u.password_hash):
            return u
        return None

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
    """Return expenses with user and category eagerly loaded so they are usable after session closes.
       If user_id provided, returns only that user's expenses."""
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

# ---------- AGGREGATION FOR GRAPH ----------
def get_expense_aggregates_by_date(user_id, days):
    """Return list of tuples (date: datetime.date, total: Decimal) for the last `days` days (including today).
       Dates with 0 total will be included (as 0)."""
    end = datetime.utcnow()
    start = end - timedelta(days=days-1)  # include today => days entries
    # Use SQL to aggregate by date (date of created_at)
    with SessionLocal() as s:
        rows = s.query(
            func.date(Expense.created_at).label("d"),
            func.coalesce(func.sum(Expense.amount), 0).label("total")
        ).filter(
            Expense.user_id == user_id,
            Expense.created_at >= start,
            Expense.created_at <= end
        ).group_by(func.date(Expense.created_at)).all()

    # rows is list of (date, total) where date is datetime.date
    # Build full date list and map totals (ensure zero-filled days)
    dates = [ (end - timedelta(days=i)).date() for i in range(days-1, -1, -1) ]  # oldest -> newest
    totals_map = {r.d: Decimal(str(r.total)) for r in rows}
    totals = [ totals_map.get(d, Decimal("0.00")) for d in dates ]
    return dates, totals

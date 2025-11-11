from typing import Optional, Annotated
from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, constr, condecimal

# -------------------------
# User
# -------------------------
UsernameType = Annotated[str, constr(min_length=1, max_length=100)]
PasswordType = Annotated[str, constr(min_length=6)]
EmailType = Optional[str]


class UserCreate(BaseModel):
    username: UsernameType
    email: EmailType = None
    password: PasswordType  # new: require a password


class UserOut(BaseModel):
    id: int
    username: str
    email: Optional[str]

    class Config:
        orm_mode = True


# -------------------------
# Category
# -------------------------
CategoryName = Annotated[str, constr(min_length=1, max_length=100)]


class CategoryCreate(BaseModel):
    name: CategoryName


class CategoryOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


# -------------------------
# Expense
# -------------------------
ExpenseName = Annotated[str, constr(min_length=1, max_length=255)]
AmountType = Annotated[Decimal, condecimal(max_digits=12, decimal_places=2)]


class ExpenseCreate(BaseModel):
    user_id: int
    category_id: int
    name: ExpenseName
    amount: AmountType


class ExpenseOut(BaseModel):
    id: int
    user_id: int
    category_id: int
    name: str
    amount: Decimal
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

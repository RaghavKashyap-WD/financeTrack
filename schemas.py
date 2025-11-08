from pydantic import BaseModel, constr, condecimal
from typing import Optional
from decimal import Decimal
from datetime import datetime

class UserCreate(BaseModel):
    username: constr(min_length=1, max_length=100)
    email: Optional[str] = None

class UserOut(BaseModel):
    id: int
    username: str
    email: Optional[str]
    class Config:
        orm_mode = True

class CategoryCreate(BaseModel):
    name: constr(min_length=1, max_length=100)

class CategoryOut(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True

class ExpenseCreate(BaseModel):
    user_id: int
    category_id: int
    name: constr(min_length=1, max_length=255)
    amount: condecimal(max_digits=12, decimal_places=2)

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

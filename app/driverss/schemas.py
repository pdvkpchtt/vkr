from datetime import date, datetime
from pydantic import BaseModel, EmailStr

from app.models.models import State


class SUserAuth(BaseModel):
    email: EmailStr
    password: str

class SGetPartsBids(BaseModel):
    id: int
    state: State

class SGetStatusBid(BaseModel):
    state: str

class SGetHistory(BaseModel):
    id: int
    date: date
    run: int
    description: str
    mechanic_id: int
    car_id: int

class SGetBid(BaseModel):
    id: int
    description: str
    state: State
    date: datetime
    mechanic_id: int
    driver_id: int

class SDriver(BaseModel):
    id: int
    name: str
    phone: int
    email: str

class SMechanic(BaseModel):
    id: int
    name: str
    phone: int
    email: str

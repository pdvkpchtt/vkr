from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from app.models.models import State


class SUserAuth(BaseModel):
    email: EmailStr
    password: str

class SGetPartsBids(BaseModel):
    id: int
    state: State
    description: str
    date: datetime

class SGetStatusBid(BaseModel):
    state: str

class SGetHistory(BaseModel):
    id: int
    date: date
    run: int
    description: str
    mechanic_id: int
    car_id: int
    work_hours: Optional[float]
    spares: Optional[str]

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
    phone: str
    email: str
    role: Optional[str]
    bithday: Optional[date]
    stag: Optional[int]

class SMechanic(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    role: Optional[str]
    bithday: Optional[date]
    stag: Optional[int]

class SMechanicForDriver(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    bithday: Optional[date]
    stag: Optional[int]

class SGetBidsForDriverWithInfoMechanic(BaseModel):
    info_bid: SGetBid
    info_mechanic: SMechanicForDriver
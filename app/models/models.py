from datetime import date
from sqlalchemy.orm import Mapped, relationship, mapped_column
from app.database import Base
from datetime import datetime
from enum import StrEnum, auto

from sqlalchemy import ForeignKey, DateTime, func


class Car(Base):
    __tablename__ = "car"
    id: Mapped[int] = mapped_column(primary_key=True)
    vin: Mapped[str] = mapped_column(unique=True)
    mark: Mapped[str]
    model: Mapped[str]
    year: Mapped[int]

    driver: Mapped["Driver"] = relationship("Driver", back_populates="car", uselist=False)
    history: Mapped[list["History"]] = relationship("History", back_populates="car")

    def __str__(self):
        return f"Car #{self.id}"

class Driver(Base):
    __tablename__ = "driver"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    phone: Mapped[int]
    email: Mapped[str]
    car_id: Mapped[int] = mapped_column(ForeignKey("car.id", ondelete="CASCADE"), unique=True)

    car: Mapped["Car"] = relationship("Car", back_populates="driver")
    bid: Mapped[list["Bid"]] = relationship("Bid", back_populates="driver")

    def __str__(self):
        return f"Driver #{self.id}"

class State(StrEnum):
    procces = auto()
    done = auto()

class Bid(Base):
    __tablename__ = "bid"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    state: Mapped[State]
    date: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    mechanic_id: Mapped[int] = mapped_column(ForeignKey("mechanic.id", ondelete="CASCADE"))
    driver_id: Mapped[int] = mapped_column(ForeignKey("driver.id", ondelete="CASCADE"))

    driver: Mapped["Driver"] = relationship("Driver", back_populates="bid")
    mechanic: Mapped["Mechanic"] = relationship("Mechanic", back_populates="bid")

    def __str__(self):
        return f"Bid #{self.id}"

class History(Base):
    __tablename__ = "history"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[date]
    run: Mapped[int]
    description: Mapped[str]
    mechanic_id: Mapped[int] = mapped_column(ForeignKey("mechanic.id", ondelete="CASCADE"))
    car_id: Mapped[int] = mapped_column(ForeignKey("car.id", ondelete="CASCADE"))

    car: Mapped["Car"] = relationship("Car", back_populates="history")
    mechanic: Mapped["Mechanic"] = relationship("Mechanic", back_populates="history")

    def __str__(self):
        return f"History #{self.id}"

class Mechanic(Base):
    __tablename__ = "mechanic"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    phone: Mapped[int]
    email: Mapped[str]

    history: Mapped[list["History"]] = relationship("History", back_populates="mechanic")
    bid: Mapped[list["Bid"]] = relationship("Bid", back_populates="mechanic")

    def __str__(self):
        return f"Mechanic #{self.id}"

class Admins(Base):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    hashed_password: Mapped[str]
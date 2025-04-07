from app.models.models import Car, Mechanic, Bid, History, Driver

from sqladmin import ModelView

class CarAdmin(ModelView, model=Car):
    column_list = [Car.id, Car.vin, Car.mark, Car.model, Car.year]
    name = "Машина"
    name_plural = "Машины"
    icon = "fa-solid fa-car"

class MechanicAdmin(ModelView, model=Mechanic):
    column_list = [Mechanic.id, Mechanic.name, Mechanic.email, Mechanic.phone]
    name = "Механик"
    name_plural = "Механики"
    icon = "fa-solid fa-mechanic"

class DriverAdmin(ModelView, model=Driver):
    column_list = [Driver.id, Driver.name, Driver.phone, Driver.email, Driver.car_id]
    name = "Водитель"
    name_plural = "Водители"
    icon = "fa-solid fa-driver"

class BidAdmin(ModelView, model=Bid):
    column_list = [Bid.id, Bid.description, Bid.state, Bid.date, Bid.driver_id, Bid.mechanic_id]
    name = "Заявка"
    name_plural = "Заявки"
    icon = "fa-solid fa-bid"

class HistoryAdmin(ModelView, model=History):
    column_list = [History.id, History.date, History.run, History.description, History.mechanic_id, History.car_id]
    name = "История"
    name_plural = "Истории"
    icon = "fa-solid fa-history"

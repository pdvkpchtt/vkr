from app.DAO.base import BaseDAO
from app.models.models import Driver, Mechanic, Admins
from app.models.models import Bid

class DriverDAO(BaseDAO):
    model = Driver

class BidDAO(BaseDAO):
    model = Bid

class AdminDAO(BaseDAO):
    model = Admins

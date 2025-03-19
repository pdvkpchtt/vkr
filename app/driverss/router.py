from fastapi import APIRouter, BackgroundTasks
# from app.driver.dao import DriverDAO, Driver
from app.driverss.daos import BidDAO
from app.exceptions import NotFound
from app.mechanic.dao import MechanicDAO
from app.models.models import State
from app.tasks.tasks import send_booking_confirmation_email

router = APIRouter(
    prefix="/driver",
)

# Класс для получения случайного механика по очереди
class MechanicAssigner:
    def __init__(self):
        self.last_mechanic_index = 0

    async def get_next_mechanic(self, mechanics):
        result = self.last_mechanic_index % (len(mechanics)) + 1
        self.last_mechanic_index += 1
        print(result)
        return result

# Создаем экземпляр класса
mechanic_assigner = MechanicAssigner()

# ручка по добавлению водителями заявки на ремонт авто
@router.post("/create_bid")
async def add_bid(
    description: str,
    background_tasks: BackgroundTasks,
):
    mechanics = await MechanicDAO.find_all()

    if not mechanics:
        raise ValueError("Нет доступных механиков")

    # Выбираем механика по индексу
    selected_mechanic = await mechanic_assigner.get_next_mechanic(mechanics)

    await BidDAO.add(
        description = description,
        state = State.procces,
        driver_id = 1,
        mechanic_id = selected_mechanic,
    )
    # Отправка на почту письма
    # res = await MechanicDAO.find_by_id(model_id=selected_mechanic)
    # background_tasks.add_task(send_booking_confirmation_email,description, res.email)


# ручка на проверки статуса
@router.get("/get_status")
async def get_status_bid(
    bid_id: int,
):

    res = await BidDAO.find_by_id(model_id=bid_id)

    if not res:
        raise NotFound

    return res.state
#odiflkgfd
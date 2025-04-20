from fastapi import FastAPI
import uvicorn

from fastapi.middleware.cors import CORSMiddleware
from app.admin.auth_admin import authentication_backend
from app.admin.views import CarAdmin, HistoryAdmin, DriverAdmin, MechanicAdmin, BidAdmin
from app.driverss.router import router as r1
from app.mechanic.router import router as r2
from app.all_routers import router as r3

from sqladmin import Admin
from app.database import engine

app = FastAPI()

admin = Admin(app, engine, authentication_backend=authentication_backend)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

admin.add_view(CarAdmin)
admin.add_view(HistoryAdmin)
admin.add_view(DriverAdmin)
admin.add_view(MechanicAdmin)
admin.add_view(BidAdmin)

# ручка по добавлению водителями заявки на ремонт авто++++++

# ручка для механика для просмотра заявок назначенных++++

# ручка для механика для редактирования статуса заявки+++

# ручка для механика для добавление истории обслуживания++++++ с привязкой к заявке

# Просмотр истории обслуживания авто





# Задачи
# 1. Админка для менеджера
# 2. Страница Водителя: ручка на добавление заявки, на просмотра статуса заявки.
# 3. Страница Механика: ручка на редактирования заявки и добавление истории.
# 4. Отправка фоновых задач механику и водителю
# 5. Добавить роли для доступа к апи. Разные точки авторизации. Войти как работодатель.

app.include_router(r1)
app.include_router(r2)
app.include_router(r3)

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)

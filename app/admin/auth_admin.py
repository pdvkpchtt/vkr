
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.auth import Auth
from app.driverss.daos import AdminDAO


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        return True

    async def logout(self, request: Request) -> bool:
        return True

    async def authenticate(self, request: Request) -> RedirectResponse | bool:
        return True


authentication_backend = AdminAuth(secret_key="...")

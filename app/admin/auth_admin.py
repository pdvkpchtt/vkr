
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.auth import Auth
from app.driverss.daos import AdminDAO


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]
        user = await Auth.authenticate_user(str(email), str(password), AdminDAO)
        if user:
            access_token = Auth.create_access_token({"sub": str(user.id), "type": "admin"})
            request.session.update({"app_token": access_token})

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> RedirectResponse | bool:
        token = request.session.get("app_token")

        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        user = await Auth.get_current_user(token)
        # logger.debug(f"{user=}")
        if not user:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
        return True


authentication_backend = AdminAuth(secret_key="...")

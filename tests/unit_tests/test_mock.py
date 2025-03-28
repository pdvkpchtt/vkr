# import pytest
# import asyncio
#
# @pytest.fixture(scope="function")  # Явно указываем область видимости
# async def event_loop():
#     loop = await asyncio.get_event_loop()
#     await loop
#     loop.close()

from fastapi import Response
from unittest.mock import AsyncMock
from app.all_routers import logout_user

# @pytest.mark.ascyncio
# @patch('app.all_routers.logout_user')
async def test_logout_user(mock_logout_user: AsyncMock):
    # mock_logout_user.return_value = None
    response = Response()
    res = await logout_user(response)
    assert res is None
    # mock_logout_user.assert_called()

# @patch('app.auth.Auth.get_current_user')
# async def test_read_users_me(
#         mock_get_current_user
# ):
#     mock_get_current_user.return_value = Admins | Mechanic | Driver
#
# class TestAuth(unittest.TestCase):
#     @patch('app.auth.Auth.get_current_user')
#     async def test_get_current_user(self, mock_get_current_user):
#         mock_get_current_user.return_value = Admins | Mechanic | Driver
#
#     @patch('app.auth.Auth.check_type_mechanic_or_driver')
#     async def test_check_type_mechanic_or_driver(self, mock_check_type_mechanic_or_driver):
#         mock_check_type_mechanic_or_driver.return_value = None

from unittest.mock import AsyncMock

import pytest

from app.all_routers import read_users_me
from app.auth import Auth
from app.models.models import Driver

@pytest.fixture(autouse=True)
async def mock_check_type():
    a = Auth()
    return AsyncMock(a, spec=Auth.check_type_mechanic_or_driver)


@pytest.mark.parametrize(
    ("user", "want"),
    [
        pytest.param(
            Driver(
                id = 3,
                name = "dsf",
                phone = 897,
                email = "das",
                car_id = 1,
            ),
            True,
        ),
    ]
)
async def test_read_users_me(user: Driver, want: bool, mock_check_type):

    # Настраиваем мок
    # mock_check_type.return_value = want

    # Вызываем функцию
    result = await read_users_me(user)

    # Проверяем вызов и результат
    mock_check_type.check_type_mechanic_or_driver.assert_called_once_with(user)
    assert result == user

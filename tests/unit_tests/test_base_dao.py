from app.driverss.daos import DriverDAO
import pytest

@pytest.mark.parametrize(
    ("name,phone,email,car_id"),
    [
        ('Пупкин Вася', 8800, 'assaa2015@mail.ru', 1, )
    ]
)
async def test_find_user_by_id(name,phone,email,car_id):
    user = await DriverDAO.find_one_or_none(email=email)

    if user:
        assert user.name == name
        assert user.phone == phone
        assert user.email == email
        assert user.car_id == car_id
    else:
        assert not user

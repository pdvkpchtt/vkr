from fastapi import HTTPException, status


class BookingException(HTTPException):  # <-- наследуемся от HTTPException, который наследован от Exception
    status_code = 500  # <-- задаем значения по умолчанию
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistException(BookingException):  # <-- обязательно наследуемся от нашего класса
    status_code=status.HTTP_409_CONFLICT
    detail="Пользователь уже существует"

class IncorrectEmailOrPasswordExceprion(BookingException):  # <-- обязательно наследуемся от нашего класса
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"

class TokenExpireException(BookingException):  # <-- обязательно наследуемся от нашего класса
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен истёк"

class TokenAbsentException(BookingException):  # <-- обязательно наследуемся от нашего класса
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутсвует"

class IncorrectTokenFormatException(BookingException):  # <-- обязательно наследуемся от нашего класса
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Некорректный формат токена"

class UserIsNotPresentException(BookingException):  # <-- обязательно наследуемся от нашего класса
    status_code=status.HTTP_401_UNAUTHORIZED

class RoomCannotBeBookes(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Не осталось свободных номеров"

class NotFound(BookingException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Не найден пользователь"




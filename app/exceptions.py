from fastapi import HTTPException, status


class AppException(HTTPException):  # <-- наследуемся от HTTPException, который наследован от Exception
    status_code = 500  # <-- задаем значения по умолчанию
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistException(AppException):  # <-- обязательно наследуемся от нашего класса
    status_code=status.HTTP_409_CONFLICT
    detail="Пользователь уже существует"

class IncorrectEmailOrPasswordExceprion(AppException):  # <-- обязательно наследуемся от нашего класса
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"

class TokenExpireException(AppException):  # <-- обязательно наследуемся от нашего класса
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен истёк"

class TokenAbsentException(AppException):  # <-- обязательно наследуемся от нашего класса
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутсвует"

class IncorrectTokenFormatException(AppException):  # <-- обязательно наследуемся от нашего класса
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Некорректный формат токена. Отсутствие доступа по роли или отсутсвие токена"

class UserIsNotPresentException(AppException):  # <-- обязательно наследуемся от нашего класса
    status_code=status.HTTP_401_UNAUTHORIZED
    detail = "Некорректный формат токена"

class RoomCannotBeBookes(AppException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Не осталось свободных номеров"

class NotFound(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Не найден пользователь"

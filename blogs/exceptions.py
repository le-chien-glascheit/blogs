from fastapi import status


class BlogsError(Exception):
    status = status.HTTP_500_INTERNAL_SERVER_ERROR
    description = 'Неизвестная ошибка'


class BlogNotFoundError(BlogsError):
    status = status.HTTP_404_NOT_FOUND
    description = 'Блог не найден'


class UserNotFoundError(BlogsError):
    status = status.HTTP_404_NOT_FOUND
    description = 'Пользователь не существует'


class PasswordMismatchError(BlogsError):
    status = status.HTTP_403_FORBIDDEN
    description = 'Не верный пароль'


class AuthorInvalidError(BlogsError):
    status = status.HTTP_400_BAD_REQUEST
    description = 'Обязательно автора или мыло'


class IncorrectDataError(BlogsError):
    status = status.HTTP_406_NOT_ACCEPTABLE
    description = 'Введёные вами данные некорректны'

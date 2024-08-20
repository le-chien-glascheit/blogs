from dataclasses import field
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class BaseUser(BaseModel):
    name: str = Field(
        default=...,
        title='Имя',
        description='Имя пользователя',
        examples=['Никита'],
    )
    email: EmailStr = Field(
        default=...,
        title='Почта',
        description='Адрес электронной почты',
        examples=['Nikita@example.com']

    )


class UserIn(BaseUser):
    password: str = Field(
        default=...,
        title='Пароль',
        description='Придумайте и введите свой пароль',
        examples=['blabla']
    )

    model_config = ConfigDict(title='Пользователь')


class UserOut(BaseUser):
    id: UUID


class PostIn(BaseModel):
    title: str = Field(
        default=...,
        title='Заголовок',
        description='Введите название вашего поста',
        examples=['Погода: свежие новости, последние события на сегодня'],
    )
    text: str = Field(
        default=...,
        title='Создать запись',
        description='Что у вас нового?',
        examples=['Жара и грозы ожидаются в Беларуси во вторник.'
                  ' При жаркой погоде учащаются случаи гибели людей на воде'
                  ' при купании и увеличивается вероятность тепловых ударов.'],
    )


class PostOut(PostIn):
    id: UUID
    author: str | None = Field(
        default=None,
        title='Автор',
        description='Имя пользователя',
        examples=['Ангелина'],
    )

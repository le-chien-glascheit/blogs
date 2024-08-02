from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class BaseUser(BaseModel):
    name: str = Field(
        title='Имя',
        description='Имя пользователя',
        examples=['Вова'],
    )
    email: EmailStr


class UserIn(BaseUser):
    password: str

    model_config = ConfigDict(title='Пользователь')


class UserOut(BaseUser):
    id: UUID


class PostIn(BaseModel):
    title: str
    text: str


class PostOut(PostIn):
    id: UUID
    author: str | None = None

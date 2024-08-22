from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import create_engine, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session as AlchemySession
from sqlalchemy.orm import sessionmaker

from blogs.exceptions import PasswordMismatchError, UserNotFoundError
from blogs.models import User
from blogs.settings import DB_URL

engine = create_engine(DB_URL)

SessionMaker = sessionmaker(engine)


def get_session():
    with SessionMaker() as session:
        yield session


Session = Annotated[AlchemySession, Depends(get_session)]

security = HTTPBasic()

Credentials = Annotated[HTTPBasicCredentials, Depends(security)]


def get_current_user(
        credentials: Credentials,
        session: Session,
) -> User:
    """Зависимость для получения текущего пользователя по BASIC авторизации."""
    try:
        user = session.execute(
            select(User).where(User.email == credentials.username),
        ).scalar_one()
    except NoResultFound as error:
        raise UserNotFoundError() from error
    else:
        if not (user.password == credentials.password):
            raise PasswordMismatchError()
        return user


CurrentUser = Annotated[User, Depends(get_current_user)]

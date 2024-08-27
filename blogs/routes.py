import types
import uuid
from enum import StrEnum
from uuid import UUID

from fastapi import APIRouter, status
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload

from blogs.dependencies import CurrentUser, Session
from blogs.exceptions import (
    IncorrectDataError,
    NotEnteredDataError,
    UserNotFoundError,
)
from blogs.models import Post, Sub, User
from blogs.schemas import PostIn, PostOut, UserIn, UserOut

BLOG_PATH = '/user'
POST_PATH = '/post'

user_router = APIRouter(prefix=BLOG_PATH, tags=['user routes'])
post_router = APIRouter(prefix=POST_PATH, tags=['post routes'])


# # - [FastAPI Basic Auth](https://fastapi.tiangolo.com/advanced/security/http-basic-auth/)


@user_router.post(
    path='',
    response_model_exclude_none=True,
    name='Зарегистрироваться',
    status_code=status.HTTP_201_CREATED,
)
def register_user(new_user: UserIn, session: Session) -> None:
    """
    Регистрация пользователей

    Введите имя пользователя, свой адрес электронной почты и придумайте пароль.
    """
    session.add(
        User(**new_user.model_dump()),
    )
    session.commit()


class SearchMode(StrEnum):
    FOLLOWERS = 'followers'
    FOLLOWED = 'followed'
    NONE = 'none'


@user_router.get(
    path='',
    name='Получить пользователей',
)
def get_users(
        session: Session,
        subscribed_to_user: UUID | None = None,
        followed: UUID | None = None,
) -> list[UserOut]:
    """
    При выборе followers выводит список всех пользователей,
    подписанных на автора, чей id вы указали.


    При выборе followed выводит список пользователей,
    на которых подписан указанный вами пользователь.

    В случае если ничего не выбрать,
    выводит всех пользователей текущей базы данных.
    """

    match type(subscribed_to_user), type(followed):
        case types.NoneType, types.NoneType:
            request = select(User)
        case uuid.UUID, types.NoneType:
            request = (
                select(User)
                .where(User.id == subscribed_to_user)
                .options(joinedload(User.followers))
            )
        case types.NoneType, uuid.UUID:
            request = (
                select(User)
                .where(User.id == followed)
                .options(joinedload(User.following))
            )
        case _:
            raise IncorrectDataError()

    if (subscribed_to_user is None) and (followed is None):
        all_users_request = session.execute(request).unique().scalars().all()
    else:
        users_request = session.execute(request).unique().scalar_one()

    target_users = []
    match type(subscribed_to_user), type(followed):
        case types.NoneType, types.NoneType:
            target_users = [
                UserOut.model_validate(user, from_attributes=True)
                for user in all_users_request
            ]
        case uuid.UUID, types.NoneType:
            target_users = [
                UserOut.model_validate(sub.follower, from_attributes=True)
                for sub in users_request.followers
            ]
        case types.NoneType, uuid.UUID:
            target_users = [
                UserOut.model_validate(sub.followed, from_attributes=True)
                for sub in users_request.following
            ]

    return target_users


@user_router.post(
    path='/{user_id}/subscribe',
    name='Подписаться на автора',
    status_code=status.HTTP_201_CREATED,
)
def subscribe_to_user(
        user_id: UUID,
        subscribing_user: CurrentUser,
        session: Session,
) -> None:
    """
    Подписаться на выбранного пользователя по id.
    """
    try:
        the_one_subscribe_to = session.execute(
            select(User).where(User.id == user_id),
        ).scalar_one()
    except NoResultFound as err:
        raise UserNotFoundError() from err

    sub = Sub(
        followed=the_one_subscribe_to,
        follower=subscribing_user,
    )
    session.add(sub)

    subscribing_user.following.append(sub)
    session.add(the_one_subscribe_to)
    session.commit()


@post_router.post(
    path='',
    response_model_exclude_none=True,
    name='Создать пост',
    status_code=status.HTTP_201_CREATED,
)
def create_post(
        post: PostIn,
        user: CurrentUser,
        session: Session,
) -> None:
    """
    Создать пост:

    Введите заголовок и текст.
    """
    new_post = Post(user=user, **post.model_dump())
    session.add(new_post)
    session.commit()


@post_router.get(
    path='',
    response_model_exclude_none=True,
    name='Получить посты',
)
def get_posts(
        session: Session,
        user_id: UUID | None = None,
) -> list[PostOut]:
    """
    Вывести все посты выбранного (по id) пользователя.
    """
    base_request = select(Post, User.name)
    if user_id is not None:
        base_request = base_request.where(Post.user_id == user_id)
    posts = session.execute(base_request.join(User))

    posts_out = []
    for post, author in posts:
        post_out = PostOut.model_validate(post, from_attributes=True)
        post_out.author = author
        posts_out.append(post_out)
    return posts_out


@user_router.patch(
    path='/{user_id}/',
    response_model_exclude_none=True,
    name='Изменить учётные данные',
)
def update_user(
        author: CurrentUser,
        session: Session,
        name: str | None = None,
        email: str | None = None,
        password: str | None = None,
) -> None:
    """
    Изменить данные вашей учётной записи

    (имя пользователя, электронную почту, пароль)
    """

    if not any((name, email, password)):
        raise NotEnteredDataError
    if name is not None:
        author.name = name
    if email is not None:
        author.email = email
    if password is not None:
        author.password = password
    session.add(author)
    session.commit()


@user_router.delete(
    path='',
    response_model_exclude_none=True,
    name='Удалить учётную запись',
)
def delete_user(
        user: CurrentUser,
        session: Session,
) -> None:
    """
    Удалить ваш аккаунт!!!
    """
    session.delete(user)
    session.commit()


@post_router.delete(
    path='',
    response_model_exclude_none=True,
    name='Удалить пост',
)
def delete_post(
        user: CurrentUser,
        session: Session,
        post_id: UUID,
) -> None:
    """
    Удалить ваш выбранный пост по его id.
    """
    post = session.execute(
        select(Post).where(Post.id == post_id).where(Post.user == user),
    ).scalar_one()
    session.delete(post)
    session.commit()

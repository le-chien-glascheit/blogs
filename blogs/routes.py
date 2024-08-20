from enum import StrEnum
from uuid import UUID

from fastapi import APIRouter, status
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload

from blogs.dependencies import CurrentUser, Session
from blogs.exceptions import IncorrectDataError, UserNotFoundError
from blogs.models import Post, Sub, User
from blogs.schemas import PostIn, PostOut, UserIn, UserOut

BLOG_PATH = '/user'
POST_PATH = '/post'

user_router = APIRouter(prefix=BLOG_PATH, tags=['user routes'])
post_router = APIRouter(prefix=POST_PATH, tags=['post routes'])


@user_router.post('', status_code=status.HTTP_201_CREATED)
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
    if (subscribed_to_user is None) and (followed is None):
        users = session.execute(select(User)).scalars().all()
        return [
            UserOut.model_validate(user, from_attributes=True)
            for user in users
        ]
    if (subscribed_to_user and followed) is not None:
        raise IncorrectDataError()

    if followed is None:
        user = (
            session.execute(
                select(User)
                .where(User.id == subscribed_to_user)
                .options(joinedload(User.followers)),
            )
            .unique()
            .scalar_one()
        )

        return [
            UserOut.model_validate(sub.follower, from_attributes=True)
            for sub in user.followers
        ]
    else:
        user = (
            session.execute(
                select(User)
                .where(User.id == followed)
                .options(joinedload(User.following)),
            )
            .unique()
            .scalar_one()
        )
        return [
            UserOut.model_validate(sub.followed, from_attributes=True)
            for sub in user.following
        ]


@user_router.post(
    path='/{user_id}/subscribe',
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
    except NoResultFound:
        raise UserNotFoundError()

    subscribing = session.execute(
        select(User).where(User.id == subscribing_user.id),
    ).scalar_one()
    sub = Sub(
        followed=the_one_subscribe_to,
        follower=subscribing,
    )
    session.add(sub)

    subscribing_user.following.append(sub)
    session.add(the_one_subscribe_to)
    session.commit()


@post_router.post('', status_code=status.HTTP_201_CREATED)
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
    if user_id is None:
        posts = session.execute(
            select(Post, User.name).join(User),
        )
        posts_out = []
        for post, author in posts:
            post_out = PostOut.model_validate(post, from_attributes=True)
            post_out.author = author
            posts_out.append(post_out)
        return posts_out
    posts = (
        session.execute(
            select(Post).where(Post.user_id == user_id),
        )
        .scalars()
        .all()
    )
    return [
        PostOut.model_validate(post, from_attributes=True)
        for post in posts
    ]


# #
# # ## Links
# # - [FastAPI Basic Auth](https://fastapi.tiangolo.com/advanced/security/http-basic-auth/)
# # user = (
# #     session.execute(
# #         select(User)
# #         .where(User.id == user_id)
# #         .options(joinedload(User.posts)),
# #     ).scalars().all()
# #
# # )
# #
# #
# @user_router.get('/{user_id}')
# def get_blog(user_id: int) -> UserOut:
#     pass
# #
# #
# # # *******************************************************************
# #
# #
# #
# #
# #
#
#
# #
# # # ******************************************************************
# #
#
# @user_router.put('/{user_id}')
# def put_blog(user_id: int, new_blog: UserIn) -> UserOut:
#     pass
# #
# #
# @user_router.patch('/{user_id}/')
# def update_blog(
#     user_id: int,
#     author: str | None = None,
#     email: EmailStr | None = None,
# ) -> None:
#     pass
# # own = (
# #     session.execute(
# #         select(User.name)
# #         .where(User.id == user_id)
# #         .options(joinedload(User.posts)),
# #     )
# #     .unique()
# #     .scalar_one()
# # )
# #
# # # *****************************************************************


@user_router.delete('', status_code=status.HTTP_204_NO_CONTENT)
def delite_user(
    user: CurrentUser,
    session: Session,
) -> None:
    """
    Удалить ваш аккаунт!!!
    """
    session.delete(user)
    session.commit()


@post_router.delete('')
def delite_post(
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

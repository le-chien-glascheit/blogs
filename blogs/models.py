from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, ForeignKey, Uuid, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    declared_attr,
    mapped_column,
    relationship,
)

from blogs.settings import settings


class Base(DeclarativeBase):
    """
    id: UUID
    """

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)

    @declared_attr
    @classmethod
    def __tablename__(cls):
        return cls.__name__.lower()


class Post(Base):
    """
    title: str
    text: str
    """

    title: Mapped[str]
    text: Mapped[str]
    user_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'))

    user: Mapped['User'] = relationship(back_populates='posts')

    def __repr__(self):
        return repr(f'{self.title} posted {self.user_id}')


class Sub(Base):
    """
    follower_id: UUID
    followed_id: UUID
    sub_date: datetime = mapped_column(default=datetime.now)
    """

    follower_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'))
    followed_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'))
    sub_date: Mapped[datetime] = mapped_column(default=datetime.now)

    follower: Mapped['User'] = relationship(
        foreign_keys='Sub.follower_id',
        back_populates='following',
    )
    followed: Mapped['User'] = relationship(
        foreign_keys='Sub.followed_id',
        back_populates='followers',
    )

    def __repr__(self):
        return repr(f'Sub id:{self.id}')


class User(Base):
    """
    name: str
    email: str
    password: str
    """

    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    posts: Mapped[list[Post]] = relationship(back_populates='user')
    followers: Mapped[list[Sub]] = relationship(
        foreign_keys='Sub.followed_id',
        back_populates='followed',
    )
    following: Mapped[list[Sub]] = relationship(
        foreign_keys='Sub.follower_id',
        back_populates='follower',
    )

    def __repr__(self):
        return repr(f'User(id={self.id}, name={self.name})')


if __name__ == '__main__':
    print('creating db')
    engine = create_engine(settings.db_url)
    Base.metadata.create_all(engine)

    user1 = User(name='vlad', email='vlad@mail.com', password='blabla')
    user2 = User(name='pasha', email='pasha@mail.com', password='blabla')
    user3 = User(name='alex', email='alex@mail.com', password='blabla')
    user4 = User(name='liza', email='liza@mail.com', password='blabla')
    user5 = User(name='avdotya', email='avdotya@mail.com', password='blabla')
    user6 = User(name='senya', email='senya@mail.com', password='blabla')
    user7 = User(name='rhaenyra', email='rhaenyra@mail.com', password='blabla')

    post1 = Post(
        title='Винипух',
        text='...в голове моей опилки...',
        user=user1,
    )

    post2 = Post(
        title='Выбил три леги в десятке',
        text='Не буду их качать, так как они для коллекции',
        user=user2,
    )

    post3 = Post(
        title='Собираю всех персонажей',
        text='осталось 5',
        user=user2,
    )

    post4 = Post(
        title='Лиза',
        text='Интересно почему у Лизы нет ни постов'
        'ни связей с другими пользователями',
        user=user3,
    )

    post5 = Post(
        title='Я есть Авдотья',
        text='Я служу своей Барыне верой и правдой',
        user=user5,
    )

    post6 = Post(
        title='Вольная',
        text='Мне она уже не к чему, тружусь ради дочки',
        user=user5,
    )

    post7 = Post(
        title='Самолетик',
        text='Отец купил мне новую игрушку...))) Лада...',
        user=user6,
    )

    post8 = Post(
        title='Про меня',
        text="""Рейенира Таргариен — персонаж вымышленного мира,
         изображённого в серии книг «Песнь Льда и Огня» Джорджа Мартина,
          королева Вестероса из валирийской династии Таргариенов,
          которая боролась за престол со своим единокровным братом Эйегоном II
           в ходе Пляски Драконов. Жена Дейемона Таргариена""",
        user=user7,
    )

    post9 = Post(
        title='Кем является Рейнира для дейнерис?',
        text="""Старший брат Визериса и Дейнерис Таргариенов,
         муж Элии Мартелл, в браке с которой родились двое
         детей — Рейнис и Эйгон. Он также является отцом
         Джона Сноу от Лианны Старк, на которой тайно женился
         после аннулирования брака с Элией.""",
        user=user7,
    )

    post10 = Post(
        title='Что стало с детьми Рейниры?',
        text="""Позже, в Битве при Глотке погиб старший сын и наследник
         Рейниры Джекейрис, а самый младший сын пропал без вести.""",
        user=user7,
    )

    post11 = Post(
        title='Почему поменяли актрису Рейниры?',
        text="""29-летнюю белокурую наследницу престола теперь грает Эмма
        Д Арси, а супругу короля — Оливия Кук. На такое решение создатели
        сериала пошли из-за скачка во времени: по словам сценаристов,
        им важно было показать, что за 10 лет героини сильно изменились.""",
        user=user7,
    )

    post12 = Post(
        title='Кто станет королем после Рейниры?',
        text="""Королём станет Эйгон |||, сын Рейниры от Деймона,
        его женой будет Джейхейра Таргариен,
        внучка Алисенты, дочь Эйгона ||""",
        user=user7,
    )

    with Session(engine) as session:
        for user in user1, user2, user3, user4, user5, user6, user7:
            session.add(user)
        for post in (
            post1,
            post2,
            post3,
            post4,
            post5,
            post6,
            post7,
            post8,
            post9,
            post10,
            post11,
            post12,
        ):
            session.add(post)

        session.commit()

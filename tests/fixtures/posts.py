import pytest

from blogs.models import Post


@pytest.fixture
def default_posts(
    session,
    user_vlad,
    user_pasha,
    user_alex,
    user_avdotya,
    user_senya,
    user_rhaenyra,
):
    post1 = Post(
        title='Винипух',
        text='...в голове моей опилки...',
        user=user_vlad,
    )
    post2 = Post(
        title='Выбил три леги в десятке',
        text='Не буду их качать, так как они для коллекции',
        user=user_pasha,
    )

    post3 = Post(
        title='Собираю всех персонажей',
        text='осталось 5',
        user=user_pasha,
    )

    post4 = Post(
        title='Лиза',
        text='Интересно почему у Лизы нет ни постов'
        'ни связей с другими пользователями',
        user=user_alex,
    )

    post5 = Post(
        title='Я есть Авдотья',
        text='Я служу своей Барыне верой и правдой',
        user=user_avdotya,
    )

    post6 = Post(
        title='Вольная',
        text='Мне она уже не к чему, тружусь ради дочки',
        user=user_avdotya,
    )

    post7 = Post(
        title='Самолетик',
        text='Отец купил мне новую игрушку...))) Лада...',
        user=user_senya,
    )

    post8 = Post(
        title='Про меня',
        text="""Рейенира Таргариен — персонаж вымышленного мира,
             изображённого в серии книг «Песнь Льда и Огня» Джорджа Мартина,
              королева Вестероса из валирийской династии Таргариенов,
              которая боролась за престол со
              своим единокровным братом Эйегоном II
               в ходе Пляски Драконов. Жена Дейемона Таргариена""",
        user=user_rhaenyra,
    )

    post9 = Post(
        title='Кем является Рейнира для дейнерис?',
        text="""Старший брат Визериса и Дейнерис Таргариенов,
             муж Элии Мартелл, в браке с которой родились двое
             детей — Рейнис и Эйгон. Он также является отцом
             Джона Сноу от Лианны Старк, на которой тайно женился
             после аннулирования брака с Элией.""",
        user=user_rhaenyra,
    )

    post10 = Post(
        title='Что стало с детьми Рейниры?',
        text="""Позже, в Битве при Глотке погиб старший сын и наследник
             Рейниры Джекейрис, а самый младший сын пропал без вести.""",
        user=user_rhaenyra,
    )

    post11 = Post(
        title='Почему поменяли актрису Рейниры?',
        text="""29-летнюю белокурую наследницу престола теперь грает Эмма
            Д Арси, а супругу короля — Оливия Кук. На такое решение создатели
            сериала пошли из-за скачка во времени: по словам сценаристов,
            им важно было показать,
            что за 10 лет героини сильно изменились.""",
        user=user_rhaenyra,
    )

    post12 = Post(
        title='Кто станет королем после Рейниры?',
        text="""Королём станет Эйгон |||, сын Рейниры от Деймона,
            его женой будет Джейхейра Таргариен,
            внучка Алисенты, дочь Эйгона ||""",
        user=user_rhaenyra,
    )

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


def create_post(session, user):
    post = Post(
        title=f'Это дополнительный пост от {user}',
        text=f'я есть {user}',
        user=user,
    )
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


@pytest.fixture
def vlad_ex_post(session, user_vlad) -> Post:
    return create_post(session, user_vlad)


@pytest.fixture
def pasha_ex_post(session, user_pasha):
    return create_post(session, user_pasha)


@pytest.fixture
def alex_ex_post(session, user_alex):
    return create_post(session, user_alex)


@pytest.fixture
def liza_ex_post(session, user_liza):
    return create_post(session, user_liza)


@pytest.fixture
def avdotya_ex_post(session, user_avdotya):
    return create_post(session, user_avdotya)


@pytest.fixture
def senya_ex_post(session, user_senya):
    return create_post(session, user_senya)


@pytest.fixture
def rhaenyra_ex_post(session, user_rhaenyra):
    return create_post(session, user_rhaenyra)

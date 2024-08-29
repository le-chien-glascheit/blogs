import pytest

from tests.conftest import User


@pytest.fixture
def user_vlad(session):
    user = User(name='vlad', email='vlad@mail.com', password='blabla')
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture
def user_pasha(session):
    user = User(name='pasha', email='pasha@mail.com', password='blabla')
    session.add(user)
    session.commit()
    return user


@pytest.fixture
def user_alex(session):
    user = User(name='alex', email='alex@mail.com', password='blabla')
    session.add(user)
    session.commit()
    return user


@pytest.fixture
def user_liza(session):
    user = User(name='liza', email='liza@mail.com', password='blabla')
    session.add(user)
    session.commit()
    return user


@pytest.fixture
def user_avdotya(session):
    user = User(name='avdotya', email='avdotya@mail.com', password='blabla')
    session.add(user)
    session.commit()
    return user


@pytest.fixture
def user_senya(session):
    user = User(name='senya', email='senya@mail.com', password='blabla')
    session.add(user)
    session.commit()
    return user


@pytest.fixture
def user_rhaenyra(session):
    user = User(name='rhaenyra', email='rhaenyra@mail.com', password='blabla')
    session.add(user)
    session.commit()
    return user


@pytest.fixture
def all_users(
    user_vlad,
    user_pasha,
    user_alex,
    user_liza,
    user_avdotya,
    user_senya,
    user_rhaenyra,
):
    pass

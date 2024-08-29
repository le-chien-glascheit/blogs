import pytest  # noqa
from fastapi.testclient import TestClient  # noqa
from sqlalchemy import create_engine, select  # noqa
from sqlalchemy.orm import sessionmaker, Session  # noqa

from blogs.main import app  # noqa
from blogs.models import Base, User, Post  # noqa
from blogs.dependencies import get_session  # noqa

engine = create_engine('sqlite:///test_db.sqlite3')
SessionMaker = sessionmaker(engine)


@pytest.fixture(autouse=True)
def _init_db():
    Base.metadata.create_all(engine)
    try:
        yield
    finally:
        Base.metadata.drop_all(engine)


def get_test_session():
    with SessionMaker() as session:
        yield session


@pytest.fixture
def session():
    with SessionMaker() as session:
        yield session


pytest_plugins = [
    'tests.fixtures.users',
    'tests.fixtures.clients',
    'tests.fixtures.posts',
]

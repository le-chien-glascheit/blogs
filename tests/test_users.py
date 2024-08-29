from sqlalchemy import select
from sqlalchemy.orm import Session  # noqa

from tests.conftest import User, select  # noqa


def test_user_register(client, session: Session):
    user_data = {
        'name': 'Никита',
        'email': 'nekit228@example.com',
        'password': '1233332blaNEKIT',
    }
    response = client.post('/user', json=user_data)
    assert response.status_code == 201
    user = session.execute(
        select(User).where(User.name == user_data['name']),
    ).scalar_one_or_none()
    assert user is not None, 'Ой, пользователя не создали'


def test_user_take_all(client, session: Session):
    response = client.get('/user')
    assert response.status_code == 200
    db_users = session.execute(select(User)).unique().scalars().all()

    assert response.json() == db_users

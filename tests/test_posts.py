from sqlalchemy import select

from tests.conftest import Post, Session, User


def test_create_post(client_vlad, session: Session, user_vlad):
    post_data = {
        'title': 'Погода сегодня',
        'text': 'Солнечная',
    }
    response = client_vlad.post(url='/post', json=post_data)
    assert response.status_code == 201
    post = session.execute(
        select(Post).where(Post.user_id == user_vlad.id),
    ).scalar_one()
    assert post.title == post_data['title']
    assert post.text == post_data['text']


def test_post_take_all(session: Session, client):
    response = client.get(url='/post')
    assert response.status_code == 200
    post = session.execute(select(Post)).unique().scalars().all()
    assert response.json() == post


#
def test_post_take(session: Session, client_vlad, user_vlad):
    response = client_vlad.get(url='/post', params={'user_id': user_vlad.id})
    assert response.status_code == 200
    post = (
        session.execute(
            select(Post, User.name)
            .where(Post.user_id == user_vlad.id)
            .join(User),
        )
        .unique()
        .scalars()
        .all()
    )
    assert response.json() == post


def test_post_delete(session: Session, client_vlad, user_vlad, vlad_ex_post):
    response = client_vlad.delete(
        url='/post',
        params={'post_id': vlad_ex_post.id},
    )

    assert response.status_code == 200, (
        f'Не корректный ответ status: {response.status_code}, '
        f'data: {response.json()}'
    )

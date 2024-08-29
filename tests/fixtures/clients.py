import pytest
from fastapi.testclient import TestClient
from httpx import BasicAuth, Client

from tests.conftest import app, get_session, get_test_session


@pytest.fixture
def client():
    app.dependency_overrides[get_session] = get_test_session
    client = TestClient(app)
    return client


@pytest.fixture
def client_vlad(user_vlad):
    app.dependency_overrides[get_session] = get_test_session
    client: Client = TestClient(app)
    client.auth = BasicAuth(
        username=user_vlad.email, password=user_vlad.password,
    )
    return client


@pytest.fixture
def client_pasha(user_pasha):
    app.dependency_overrides[get_session] = get_test_session
    client: Client = TestClient(app)
    client.auth = BasicAuth(
        username=user_pasha.email, password=user_pasha.password,
    )
    return client


@pytest.fixture
def client_alex(user_alex):
    app.dependency_overrides[get_session] = get_test_session
    client: Client = TestClient(app)
    client.auth = BasicAuth(
        username=user_alex.email, password=user_alex.password,
    )
    return client


@pytest.fixture
def client_liza(user_liza):
    app.dependency_overrides[get_session] = get_test_session
    client: Client = TestClient(app)
    client.auth = BasicAuth(
        username=user_liza.email, password=user_liza.password,
    )
    return client


@pytest.fixture
def client_avdotya(user_avdotya):
    app.dependency_overrides[get_session] = get_test_session
    client: Client = TestClient(app)
    client.auth = BasicAuth(
        username=user_avdotya.email, password=user_avdotya.password,
    )
    return client


@pytest.fixture
def client_senya(user_senya):
    app.dependency_overrides[get_session] = get_test_session
    client: Client = TestClient(app)
    client.auth = BasicAuth(
        username=user_senya.email, password=user_senya.password,
    )
    return client


@pytest.fixture
def client_rhaenyra(user_rhaenyra):
    app.dependency_overrides[get_session] = get_test_session
    client: Client = TestClient(app)
    client.auth = BasicAuth(
        username=user_rhaenyra.email, password=user_rhaenyra.password,
    )
    return client

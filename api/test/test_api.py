import pytest

from api.api import app
from resources.auth_token import AuthTokenFactory
from resources.const import MOVIE_DATASET, HEADER_AUTH_TOKEN, AUTH_FACTORY


@pytest.fixture
def client():
    # setup db
    app.config[MOVIE_DATASET] = "small"
    app.config[AUTH_FACTORY] = AuthTokenFactory(private_key="some key")
    client = app.test_client()

    yield client

    # cleanup db
    pass


def test_unauthenticated_get(client):
    resp = client.get("/movies")
    assert resp.status_code == 401


def test_generate_token_failure(client):
    resp = client.post("/token/generate", data={})
    assert resp.status_code == 401


def test_generate_token_success(client):
    resp = client.post("/token/generate", data={
        "username": "user",
        "password": "test1",
    })
    assert resp.status_code == 201
    token = resp.json["token"]

    resp2 = client.get("/movies", headers={
        HEADER_AUTH_TOKEN: token,
    })
    assert resp2.status_code == 200


def test_validate_token(client):
    resp = client.post("/token/generate", data={
        "username": "user",
        "password": "test1",
    })
    assert resp.status_code == 201
    token = resp.json["token"]

    resp2 = client.post("/token/validate", data={
        "token": token
    })
    assert resp2.status_code == 200
    j = resp2.json
    print(j)


if __name__ == '__main__':
    pytest.main(["test_api.py", "-k", "test_valid"])

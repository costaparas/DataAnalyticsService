import os
import tempfile

import pytest
from api.api import app
from resources.const import MOVIE_DATASET, HEADER_AUTH_TOKEN


@pytest.fixture
def client():
    #setup db
    app.config[MOVIE_DATASET] = "small"
    client = app.test_client()

    yield client

    #cleanup db
    pass

@pytest.mark.skip()
def test_get_a_movie(client):
    resp = client.get("/movies/0114709")
    assert resp.status_code == 200
    print(resp)

def test_generate_token_failure(client):
    resp = client.get("/token/generate", data={ })
    assert resp.status_code == 401
def test_generate_token_success(client):
    resp = client.get("/token/generate", data={
        "username": "user",
        "password" : "test1",
    })
    assert resp.status_code == 200
    token = resp.json()["token"]

    resp2 = client.get("/movies/",headers={
        HEADER_AUTH_TOKEN : token,
    })
    assert resp2.status_code == 200

if __name__ == '__main__':
    pytest.main(["test_api.py"])


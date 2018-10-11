import os
import tempfile

import pytest
from api import app, MOVIE_DATASET


@pytest.fixture
def client():
    #setup db
    app.config[MOVIE_DATASET] = "small"
    client = app.test_client()

    yield client

    #cleanup db
    pass

def test_a(client):
    resp = client.get("/movies/0114709")
    print(resp)

if __name__ == '__main__':
    pytest.main(["test_api.py"])


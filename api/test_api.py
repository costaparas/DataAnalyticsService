import os
import tempfile

import pytest
from api import app


@pytest.fixture
def client():
    #setup db
    client = app.test_client()

    yield client

    #cleanup db
    pass

def test_a(client):
    resp = client.get("/movies/1")
    print(resp)

if __name__ == '__main__':
    pytest.main(["test_api.py"])


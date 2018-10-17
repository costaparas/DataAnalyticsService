import pytest

from client.api_client import ApiClient, RequestFailure


@pytest.fixture
def client():
    yield ApiClient(server_url=SERVER_URL)


SERVER_URL = "https://movie-recommender-api.herokuapp.com"


def test_get_token():
    api_client = ApiClient(server_url=SERVER_URL)
    assert api_client.validate_own_token()


def test_init_with_invalid_token():
    api_client = ApiClient(server_url=SERVER_URL, token="asdf")
    assert api_client.validate_own_token()


def test_get_movies(client):
    movies = client.get_movies(limit=2)
    assert len(movies) == 2


def test_get_valid_movie(client):
    movie = client.get_movie(movie_id="0057261")
    assert movie["Title"] == "Lord of the Flies"


def test_get_invalid_movie(client):
    with pytest.raises(RequestFailure):
        movie = client.get_movie(movie_id="not a real movie id")


if __name__ == '__main__':
    pytest.main(["test_api_client.py"])

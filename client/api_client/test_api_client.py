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


def test_get_movie_by_title(client):
    movie = client.get_movie_by_title(movie_title="lord of the flies")
    assert movie["movie_id"] == "0057261"

    #This needs to be fixed on backend.
    #Search should be case insensitive
    movie2 = client.get_movie_by_title(movie_title="Lord of the Flies")
    assert movie2["movie_id"] == "0057261"
def test_get_invalid_movie(client):
    with pytest.raises(RequestFailure):
        movie = client.get_movie(movie_id="not a real movie id")
def test_get_movie_recommendations_by_id(client):
    recoms = client.get_movie_recommendations_by_id(movie_id="0057261")
    assert len(recoms) >= 0


def test_get_movie_recommendations_by_title(client):
    recoms = client.get_movie_recommendations_by_title(movie_title="lord of the flies",limit=5)
    assert 0 <= len(recoms) <=5
if __name__ == '__main__':
    # pytest.main(["test_api_client.py", "-k", "test_get_movie_by_title"])
    # pytest.main(["test_api_client.py", "-k", "test_get_movie_recom"])
    pytest.main(["test_api_client.py"])

import pytest

from api.api import app
from resources.auth_token import AuthTokenFactory
from resources.const import MOVIE_DATASET, HEADER_AUTH_TOKEN, AUTH_FACTORY


@pytest.fixture
def client():
    # setup db
    app.config[MOVIE_DATASET] = "full"
    app.config[AUTH_FACTORY] = AuthTokenFactory(private_key="some key")
    client = app.test_client()

    yield client

    # cleanup db
    pass


def get_token(client):
    resp = client.post("/token/generate", data={
        "username": "user",
        "password": "test1",
    })
    assert resp.status_code == 201
    token = resp.json["token"]
    return token

def test_search_movies_by_title_b(client):
    token = get_token(client=client)
    resp = client.get("/movies", headers={
        HEADER_AUTH_TOKEN: token,
    }, data={
        "inTitle": "Lord of the Flies",
        "limit": 1,
    })
    assert resp.status_code == 200

    assert len(resp.json["movies"]) == 1
    assert resp.json["movies"][0]["movie_id"] == "0057261"

    resp2 = client.get("/movies", headers={
        HEADER_AUTH_TOKEN: token,
    }, data={
        "inTitle": "lord of the flies",
        "limit": 1,
    })
    assert resp2.status_code == 200
    assert len(resp2.json["movies"]) == 1
    assert resp.json["movies"][0]["movie_id"] == "0057261"


def test_search_movies_by_title(client):
    token = get_token(client=client)
    resp = client.get("/movies", headers={
        HEADER_AUTH_TOKEN: token,
    }, data={
        "sortBy":"top-rated",
        # "sortBy":"oldest",
        "genre" : "Drama",
        # "sortBy": "title",
        # "inTitle": "dog",
        "limit": 20,
    })
    assert resp.status_code == 200
    j = resp.json
    print(j)

def test_get_titles(client):
    token = get_token(client=client)
    resp = client.get("/movie_titles", headers={
        HEADER_AUTH_TOKEN: token,
    })
    j = resp.json
    assert resp.status_code == 200
    assert "movies" in j
    movies = j["movies"]
    weird_years = []
    for movie in movies:
        year = movie["year"]
        if not(year.startswith("1") or year.startswith("2")):
            print(movie)
        try:
            _ = int(movie["year"])
        except ValueError:
            weird_years.append(movie)
    print(weird_years)
def test_get_genres(client):
    token = get_token(client=client)
    resp = client.get("/genres", headers={
        HEADER_AUTH_TOKEN: token,
    })
    j = resp.json
    assert resp.status_code == 200


def test_get_random_movies(client):
    token = get_token(client=client)
    resp = client.get("/random/movies", headers={
        HEADER_AUTH_TOKEN: token,
    }, data={
        "limit": 2,
    })
    j = resp.json
    assert resp.status_code == 200


def test_get_recommendation(client):
    token = get_token(client=client)
    resp2 = client.get("/recommendations/0098282", headers={
        HEADER_AUTH_TOKEN: token,
    },data={
        "limit" : 5,
    })
    j = resp2.json
    assert resp2.status_code == 200
    assert 'recommendations' in j
    assert len(j['recommendations']) <= 5


def test_unauthenticated_get(client):
    resp = client.get("/movies")
    assert resp.status_code == 401


def test_generate_token_failure(client):
    resp = client.post("/token/generate", data={})
    assert resp.status_code == 400


def test_generate_token_success(client):
    token = get_token(client=client)
    resp2 = client.get("/movies", headers={
        HEADER_AUTH_TOKEN: token,
    })
    assert resp2.status_code == 200


def test_validate_token(client):
    token = get_token(client)
    resp2 = client.post("/token/validate", data={
        "token": token
    })
    assert resp2.status_code == 200
    j = resp2.json
    print(j)

def test_duplicate_titles(client):
    token = get_token(client=client)
    resp = client.get("/movie_titles", headers={
        HEADER_AUTH_TOKEN: token,
    })
    assert resp.status_code == 200
    j = resp.json
    movies = j["movies"]
    from collections import Counter
    titles_dict = Counter()
    for movie in movies:
        key = movie["title"] + movie["year"]
        titles_dict[key] +=1
    duplicates = [
        (title,count) for title,count in titles_dict.items() if count>1
    ]
    print(duplicates)

if __name__ == '__main__':
    # pytest.main(["test_api.py", "-k", "test_get_titles"])
    # pytest.main(["test_api.py", "-k", "test_duplicate_titles"])
    pytest.main(["test_api.py"])

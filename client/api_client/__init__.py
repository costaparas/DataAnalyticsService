import requests

GET = "GET"
POST = "POST"


class RequestFailure(Exception):
    def __init__(self, response, msg="Request failed."):
        super(RequestFailure, self).__init__("{}. Response={}".format(msg, response))
        self.response = response


class MovieSortCriteria:
    RELEASE_OLDEST = "oldest"
    RELEASE_NEWEST = "newest"
    TITLE = "title"
    TOP_RATED = "top-rated"
    all_criteria = [TOP_RATED, TITLE, RELEASE_NEWEST, RELEASE_OLDEST]


class ApiClient:
    def __init__(self, server_url, token=None):
        self.server_url = server_url
        self.session = requests.Session()
        if token is None:
            self.token = self.get_new_token()
        else:
            self.token = token
            if not self.validate_own_token():
                self.token = self.get_new_token()

    def make_authenticated_request(self, method, url, headers=None, **kwargs):
        auth_header = {
            "Auth-Token": self.token
        }
        all_headers = auth_header.copy()
        if type(headers) is dict:
            all_headers.update(headers)
        req = requests.Request(method=method, url=url, headers=all_headers, **kwargs)
        prepped = self.session.prepare_request(req)

        return self.session.send(prepped)

    def get_genres(self):
        resp = self.make_authenticated_request(
            GET,
            self.build_url("/genres")
        )
        if resp.status_code == 200:
            genres = resp.json()["genres"]
            return genres
        else:
            raise RequestFailure(resp)

    def get_movie(self, movie_id):
        resp = self.make_authenticated_request(
            GET,
            self.build_url("/movies/{}".format(movie_id))
        )

        if resp.status_code == 200:
            j = resp.json()
            return j
        else:
            raise RequestFailure(resp)

    def get_movies(self, limit=None, sort_by=MovieSortCriteria.TOP_RATED, **kwargs):
        params = {
            "sortBy": sort_by,
        }
        if limit is not None:
            params["limit"] = limit

        params.update(**kwargs)

        resp = self.make_authenticated_request(
            GET,
            self.build_url("/movies"),
            data=params)
        if resp.status_code == 200:
            movie_list = resp.json()["movies"]
            return movie_list
        else:
            raise RequestFailure(resp)

    def get_random_movies(self, limit=10):
        resp = self.make_authenticated_request(
            GET,
            self.build_url("/random/movies"),
            data={
                "limit": limit,
            })
        if resp.status_code == 200:
            movie_list = resp.json()["movies"]
            return movie_list
        else:
            raise RequestFailure(resp)

    def get_movie_names(self):
        params = {
            "sortBy": MovieSortCriteria.TITLE,
            "format" : "minimal"
        }
        resp = self.make_authenticated_request(
            GET,
            self.build_url("/movies"),
            data=params)
        if resp.status_code == 200:
            movie_list = resp.json()["movies"]
            return movie_list
        else:
            raise RequestFailure(resp)

    def get_movie_recommendations_by_id(self, movie_id, limit=10):
        resp = self.make_authenticated_request(
            GET,
            self.build_url("/recommendations/{}".format(movie_id)),
            data={
                "limit": limit,
            })
        if resp.status_code == 200:
            j = resp.json()
            recom = j["recommendations"]
            return recom
        else:
            raise RequestFailure(resp)

    def build_url(self, api_path):
        return self.server_url + api_path

    def get_new_token(self, username="user", password="test1"):
        """

        # Default credentials are a valid set of credentials.
        :param username:
        :param password:
        :return: token as a string
        """
        resp = requests.post(self.build_url("/token/generate"), data={
            "username": username,
            "password": password,
        })
        if resp.status_code == 201:
            token = resp.json()["token"]
            return token
        else:
            raise RequestFailure(resp, msg="Could not generate new token.")

    def validate_own_token(self):
        resp = requests.post(self.build_url("/token/validate"), data={
            "token": self.token,
        })
        if resp.status_code == 200:
            j = resp.json()
            return j["token_status"] == "valid"
        else:
            raise RequestFailure(resp, msg="Could not validate token.")

import requests


class RequestFailure(Exception):
    def __init__(self, response, msg="Request failed."):
        super(RequestFailure, self).__init__("{}. Response={}".format(msg, response))
        self.response = response


class ApiClient:
    def __init__(self, server_url, token=None):
        self.server_url = server_url
        if token is None:
            self.token = self.get_new_token()
        else:
            self.token = token
            if not self.validate_own_token():
                self.token = self.get_new_token()

    def get_movie(self, movie_id):
        resp = requests.get(self.build_url("/movies/{}".format(movie_id)), headers={
            "Auth-Token": self.token
        })
        if resp.status_code == 200:
            j = resp.json()
            return j
        else:
            raise RequestFailure(resp)

    def get_movies(self, limit=10):
        resp = requests.get(self.build_url("/movies"), headers={
            "Auth-Token": self.token
        }, data={
            "limit": limit
        })
        if resp.status_code == 200:
            movie_list = resp.json()["movies"]
            return movie_list
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

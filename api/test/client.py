import requests


def build_url(api_path):
    # Change this if you change the server port.
    server_url = "http://localhost:5001"
    return server_url + api_path


def generate_token():
    resp = requests.post(build_url("/token/generate"), data={
        # This is a valid set of credentials.
        "username": "user",
        "password": "test1",
    })
    if resp.status_code == 201:
        token = resp.json()["token"]
        return token


def token_is_valid(token):
    resp = requests.post(build_url("/token/validate"), data={
        "token": token,
    })
    if resp.status_code == 200:
        token_status = resp.json()["token_status"]
        return token_status == "valid"
    return False


def get_movie_list(token):
    resp = requests.get(build_url("/movies"), headers={
        "Auth-Token": token
    })
    if resp.status_code == 200:
        movie_list = resp.json()["movies"]
        return movie_list
    else:
        # Auth failure (bad token)
        pass


if __name__ == '__main__':
    token = generate_token()
    print("Token: {}".format(token))
    print("Movies: {}".format(get_movie_list(token)))

    # if you want to check a token is valid:
    is_valid = token_is_valid(token)
    print("Token valid? {}".format(is_valid))

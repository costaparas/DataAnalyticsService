import json
import flask
import os

from resources.const import MOVIE_DATASET


def get_this_dir():
    path_of_this_script = os.path.realpath(__file__)
    dir_ = os.path.dirname(path_of_this_script)
    return dir_


def get_movie_data():
    import flask
    if flask.has_app_context():
        dataset = flask.current_app.config.get(MOVIE_DATASET)
    else:
        dataset = "full"

    if dataset == "full":
        return get_movie_data_full()
    elif dataset == "small":
        return get_movie_data_small()
    else:
        raise Exception("Invalid movie dataset config.")
def get_movie_data_from_file(filename):
    path = os.path.abspath(os.path.join(get_this_dir(), "../data", filename))
    return json.load(open(path, encoding="utf8"))


def get_movie_data_small():
    file = "movies-small.json"
    return get_movie_data_from_file(file)


def get_movie_data_full():
    file = "movies-full.json"
    return get_movie_data_from_file(file)

import json
import os


def get_this_dir():
    path_of_this_script = os.path.realpath(__file__)
    dir_ = os.path.dirname(path_of_this_script)
    return dir_


def get_movie_data(filename):
    path = os.path.abspath(os.path.join(get_this_dir(), "../data", filename))
    return json.load(open(path, encoding="utf8"))


def get_movie_data_small():
    file = "movies-small.json"
    return get_movie_data(file)


def get_movie_data_full():
    file = "movies-full.json"
    return get_movie_data(file)

import flask
from flask import Flask, render_template, request, url_for, redirect

import os,sys
def get_this_dir(file):
    path_of_this_script = os.path.realpath(file)
    dir_ = os.path.dirname(path_of_this_script)
    return dir_


def mod_syspath(file):
    path_to_append = get_this_dir(file)
    path_to_append = os.path.join(path_to_append, "..")
    path_to_append = os.path.abspath(path_to_append)
    sys.path.append(path_to_append)
    print(sys.path)

mod_syspath(__file__)

from api_client import ApiClient

CONFIG_API_CLIENT = "api client"
app = Flask(__name__)
app.config['SECRET_KEY'] = '3c6bf310da9102a0762ea238236cba3b'
app.config[CONFIG_API_CLIENT] = ApiClient(
    server_url="https://movie-recommender-api.herokuapp.com"
)

def get_api_client():
    return flask.current_app.config[CONFIG_API_CLIENT]



@app.route('/')
def index():
    return render_template('template.html')



if __name__ == '__main__':
	app.run(debug=True)
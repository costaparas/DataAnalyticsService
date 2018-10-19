import argparse

import flask
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import SubmitField

from api_client import ApiClient

HEROKU_API_SERVER = "https://movie-recommender-api.herokuapp.com"
CONFIG_API_CLIENT = "api client"

app = Flask(__name__)
app.config['SECRET_KEY'] = '3c6bf310da9102a0762ea238236cba3b'


def get_api_client():
    return flask.current_app.config[CONFIG_API_CLIENT]


@app.route('/search', methods=['GET', 'POST'])
def search():
    raise NotImplementedError


# movie_name = request.form['search_term']
# movie_list = get_api_client().get_movies(limit=20)
# # movie_name_list = get_api_client().get_movie_names()
# return render_template('template-results.html', searched_term=movie_name, movies=movie_list, movie_names=movie_name_list)


@app.route('/')
def index():
    search_form = searchForm()
    random_movies = get_api_client().get_random_movies(limit=15)
    movie_name_list = get_api_client().get_movie_names()
    return render_template('template.html', form=search_form, movies=random_movies, movie_names=movie_name_list)


class searchForm(FlaskForm):
    submit_button = SubmitField('search')




def parse_cmd_line_args():
    parser = argparse.ArgumentParser(description='Run web-app UI server.')
    parser.add_argument("--port", "-p", type=int, default=5000)
    parser.add_argument("--api_url","-u", type=str, default=HEROKU_API_SERVER)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_cmd_line_args()
    app.config[CONFIG_API_CLIENT] = ApiClient(
        server_url=args.api_url
    )
    print(args)
    app.run(debug=True,port=args.port)

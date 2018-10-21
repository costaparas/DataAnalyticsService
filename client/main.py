import argparse
import json
import secrets

import flask
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

from api_client import ApiClient, RequestFailure

CONFIG_API_CLIENT = "api client"

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe()
app.config['APP_NAME'] = 'MovieTime'

def get_api_client():
    return flask.current_app.config[CONFIG_API_CLIENT]

@app.route('/movies/<string:movie_id>', methods=["GET"])
def view_movie(movie_id):
    try:
        movie = get_api_client().get_movie(movie_id)
        recom = get_api_client().get_movie_recommendations_by_id(movie_id, limit=24)
        return flask.render_template(
            "movies.html",
            base_movie=movie,
            movies=recom
        )
    except RequestFailure:
        flask.abort(404)

@app.route('/')
def home():
    random_movies = get_api_client().get_random_movies(limit=20)
    movie_name_list = get_api_client().get_movie_names()
#    movie_list_json = json.dumps(movie_name_list)
    posters = list(map(lambda x: (x['Poster'], x['movie_id']), random_movies))
    return render_template(
        'home.html',
        posters=posters#,
#        autocomplete=movie_list_json
    )

def parse_cmd_line_args():
    HEROKU_API_SERVER = "https://movie-recommender-api.herokuapp.com"
    parser = argparse.ArgumentParser(description='Run web-app UI server.')
    parser.add_argument("--port", "-p", type=int, default=5000)
    parser.add_argument("--api_url", "-u", type=str, default=HEROKU_API_SERVER)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_cmd_line_args()
    app.config[CONFIG_API_CLIENT] = ApiClient(
        server_url=args.api_url
    )
    print(args)

    # override port number with environment variable
    # this approach is used in the deployed api
    import os
    if 'PORT' in os.environ:
        port = os.environ['PORT']

    app.run(debug=True, port=args.port, host='0.0.0.0')

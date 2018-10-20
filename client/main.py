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


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        in_title = form.in_title.data
        movies = get_api_client().get_movies(inTitle=in_title)
        # return "Searched: {}".format(form.in_title.data)
        return flask.render_template("search_results.html",
                                     movies=movies,
                                     query=in_title)
    else:
        return flask.redirect(flask.url_for('home'))

@app.route('/movies/<string:movie_id>', methods=["GET"])
def view_movie(movie_id):
    search_form = SearchForm()
    try:
        movie = get_api_client().get_movie(movie_id)
        recom = get_api_client().get_movie_recommendations_by_id(movie_id, limit=20)
        return flask.render_template(
            "view_movie.html",
            base_movie=movie,
            form=search_form,
            movies=recom

        )
    except RequestFailure:
        flask.abort(404)


@app.route('/')
def home():
    search_form = SearchForm()
    random_movies = get_api_client().get_random_movies(limit=15)
    movie_name_list = get_api_client().get_movie_names()
    movie_list_json = json.dumps(movie_name_list)
    return render_template('home.html',
                           form=search_form,
                           random_movies=random_movies,
                           movie_list_json=movie_list_json
                           )


class SearchForm(FlaskForm):
    in_title = StringField('in_title', validators=[DataRequired()])
    # submit_button = SubmitField('search')


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
    app.run(debug=True, port=args.port)

import flask
from flask import Flask, render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

from api_client import ApiClient

CONFIG_API_CLIENT = "api client"
app = Flask(__name__)
app.config['SECRET_KEY'] = '3c6bf310da9102a0762ea238236cba3b'
app.config[CONFIG_API_CLIENT] = ApiClient(
    server_url="https://movie-recommender-api.herokuapp.com"
)

def get_api_client():
    return flask.current_app.config[CONFIG_API_CLIENT]

@app.route('/search', methods=['GET', 'POST'])
def search():
	movie_name = request.form['search_term']
	movie_list = get_api_client().get_movie_recommendations_by_title(movie_title=movie_name,limit=20)
	return render_template('template-results.html', searched_term=movie_name, movies=movie_list)


@app.route('/')
def index():
	search_form = searchForm()
	movie_list = get_api_client().get_random_movies(limit=15)
	movie_name_list = get_api_client().get_movie_names()
	return render_template('template.html', form=search_form, movies=movie_list, movie_names=movie_name_list)


class searchForm(FlaskForm):
	search_term =  StringField('Movie Title', validators=[DataRequired()])
	submit_button = SubmitField('search')


if __name__ == '__main__':
	app.run(debug=True)
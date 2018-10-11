import argparse

from flask import Flask
from flask_restplus import Api, Resource

MOVIE_DATASET = "movie_dataset"
from movie_data import get_movie_data_small, get_movie_data_full

app = Flask(__name__)
api = Api(app,
          title="Movie Recommendation API",
          description="This API provides access to a database of movie titles, information about each title and movie recommendations.",
          version="1.0"
          )
api.namespaces.clear()
movies_ns = api.namespace("movies", description="")
recommendations_ns = api.namespace("recommendations", description="")


def get_movie_data():
    dataset = app.config.get(MOVIE_DATASET)
    if dataset == "full":
        return get_movie_data_full()
    elif dataset == "small":
        return get_movie_data_small()
    else:
        raise Exception("Invalid movie dataset config.")


@movies_ns.route('/<string:movie_id>')
class Movie(Resource):
    def get(self, movie_id):
        movie_data = get_movie_data()
        if movie_id in movie_data:
            return movie_data[movie_id]
        else:
            api.abort(404)


@movies_ns.route('')
class MovieList(Resource):
    def get(self):
        movie_data = get_movie_data()
        movie_ids = list(movie_data.keys())
        return {
            'movies': movie_ids,
            'num_movies' : len(movie_ids)
        }


@recommendations_ns.route('/<string:movie_id>')
class Recommendations(Resource):
    def get(self, movie_id):
        return {}
        # if movie_id in movie_data:
        #     return {
        #         'movie_id': movie_id,
        #         'recommendations': []
        #     }
        # else:
        #     api.abort(404)


def run_from_cmd_line(app):
    parser = argparse.ArgumentParser(description='Run api server.')
    parser.add_argument("--port", "-p", type=int, default=5001)
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--dataset", choices=("full", "small"), default="small")
    args = parser.parse_args()
    print(args)
    app.config[MOVIE_DATASET] = args.dataset
    app.run(debug=args.debug, port=args.port)


if __name__ == '__main__':
    run_from_cmd_line(app=app)
    # import os
    # print(os.getcwd())
    # print(list(get_movie_data_small().items())[:1])

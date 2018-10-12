from flask import Flask
from flask_restplus import Api

app = Flask(__name__)
api = Api(app,
          title="Movie Recommendation API",
          description="This API provides access to a database of movie titles, information about each title and movie recommendations.",
          version="1.0"
          )
api.namespaces.clear()
movies_ns = api.namespace("movies", description="")
recommendations_ns = api.namespace("recommendations", description="")

from resources import Movie, MovieList, Recommendations

movies_ns.add_resource(Movie, '/<string:movie_id>')
movies_ns.add_resource(MovieList, '')
recommendations_ns.add_resource(Recommendations, '/<string:movie_id>')


def run_from_cmd_line(app):
    import argparse
    from movie_data import MOVIE_DATASET
    parser = argparse.ArgumentParser(description='Run api server.')
    parser.add_argument("--port", "-p", type=int, default=5001)
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--dataset", choices=("full", "small"), default="small")
    parser.add_argument("--key", type=str, default=None, help="Path to private key. If no key is specified then API auth is disabled.")
    args = parser.parse_args()
    print(args)
    app.config[MOVIE_DATASET] = args.dataset
    app.run(debug=args.debug, port=args.port)


if __name__ == '__main__':
    run_from_cmd_line(app=app)

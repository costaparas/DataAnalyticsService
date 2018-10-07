from flask import Flask
from flask_restplus import Api, Resource

from mockdata import movie_data

app = Flask(__name__)
api = Api(app,
          title="Movie Recommendation API",
          description="This API provides access to a database of movie titles, information about each title and movie recommendations.",
          version="1.0"
          )
api.namespaces.clear()
movies_ns = api.namespace("movies", description="")
recommendations_ns = api.namespace("recommendations", description="")


@movies_ns.route('/<string:movie_id>')
class Movie(Resource):
    def get(self, movie_id):
        if movie_id in movie_data:
            return movie_data[movie_id]
        else:
            api.abort(404)


@movies_ns.route('')
class MovieList(Resource):
    def get(self):
        return {'movies': list(movie_data.values())}


@recommendations_ns.route('/<string:movie_id>')
class Recommendations(Resource):
    def get(self, movie_id):
        if movie_id in movie_data:
            return {
                'movie_id': movie_id,
                'recommendations': []
            }
        else:
            api.abort(404)


if __name__ == '__main__':
    app.run(debug=True)

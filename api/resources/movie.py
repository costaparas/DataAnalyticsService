from flask_restplus import abort, Resource, Namespace
from .requires_auth import requires_auth
from movie_data import get_movie_data

api = Namespace("movies", description="Movie data.")

def get_movie_or_404(movie_id):
    movie_data = get_movie_data()
    if movie_id in movie_data:
        return movie_data[movie_id]
    else:
        abort(404, "Movie not found.")

@api.route('/<string:movie_id>')
class Movie(Resource):
    @api.response(200, 'Movie found.')
    @api.response(404, 'Movie not found.')
    @api.doc(description="Get information about a particular movie.")
    @requires_auth(api)
    def get(self, movie_id):
        return get_movie_or_404(movie_id)


@api.route('')
class MovieList(Resource):
    @api.response(200, 'Success.')
    @api.doc(description="Get available movies as a list of movie IDs.")
    @requires_auth(api)
    def get(self):
        movie_data = get_movie_data()
        movie_ids = list(movie_data.keys())
        return {
            'movies': movie_ids,
            'num_movies': len(movie_ids)
        }
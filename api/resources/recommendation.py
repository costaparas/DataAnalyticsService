from flask_restplus import Resource, Namespace

from resources.movie import get_movie_or_404
from resources.requires_auth import requires_auth

api = Namespace("recommendations", description="Movie recommendations.")

@api.param("movie_id", "Movie ID")
@api.route('/<string:movie_id>')
class Recommendations(Resource):

    @api.response(200, 'Success.')
    @api.response(404, 'Movie not found.')
    @api.doc(description="Get recommendations for a given movie.")
    @requires_auth(api)
    def get(self, movie_id):
        movie = get_movie_or_404(movie_id)
        return {
                'movie_id' : movie_id,
                'movie' : movie,
                'recommendations': []
            }
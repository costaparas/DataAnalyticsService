from flask_restplus import Resource, Namespace

from resources.movie import get_movie_or_404, get_movie_info
from resources.requires_auth import requires_auth

import sys
sys.path.append('../ml')
import recommend

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
        recommendations = map(recommend.recommend(movie['Title'])['cluster_movies'], lambda x: x['id'])
        return {
                'movie_id' : movie_id,
                'movie' : movie,
                'recommendations': get_movie_info(recommendations)
            }

from flask_restplus import Resource, Namespace

from resources.movie import get_movie_or_404, get_movies_info
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
        cluster_data = ['../ml/clusters.pk', '../ml/cluster-numbers.pk']
        recommendation_data = recommend.recommend(movie['Title'], cluster_data)['cluster_movies']
        recommendations = list(map(lambda x: x['id'], recommendation_data))
        recommendations.remove(movie_id)
        return {
                'movie_id' : movie_id,
                'movie' : movie,
                'num_recommendations' : len(recommendations),
                'recommendations': get_movies_info(recommendations)
            }

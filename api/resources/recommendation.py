from flask_restplus import Resource, Namespace, reqparse

from resources.movie import get_movie_or_404, get_movies_info
from resources.requires_auth import requires_auth

import sys, os
from resources.utils import get_this_dir, append_ml_dir_to_syspath

append_ml_dir_to_syspath(__file__)
# sys.path.append(os.path.join('..', 'ml'))
import recommend

api = Namespace("recommendations", description="Movie recommendations.")

movie_recom_req_parser = reqparse.RequestParser()
movie_recom_req_parser.add_argument('limit', type=int, help="Limit number of recommendation results.", default=10)
@api.param("movie_id", "Movie ID")
@api.route('/<string:movie_id>')
class Recommendations(Resource):

    @api.response(200, 'Success.')
    @api.response(404, 'Movie not found.')
    @api.doc(description="Get movie recommendations based on a given movie.")
    @requires_auth(api)
    @api.expect(movie_recom_req_parser)
    def get(self, movie_id):
        movie = get_movie_or_404(movie_id)
        ml_dir = os.path.abspath(os.path.join(get_this_dir(__file__), "../../ml"))
        clusters_path = os.path.abspath(os.path.join(ml_dir,"clusters.pk"))
        cluster_numbers_path = os.path.abspath(os.path.join(ml_dir,"cluster-numbers.pk"))

        cluster_data = [clusters_path, cluster_numbers_path]
        # cluster_data = [os.path.join('..', 'ml', 'clusters.pk'), os.path.join('..', 'ml', 'cluster-numbers.pk')]
        recommendation_data = recommend.recommend(movie['Title'], cluster_data)['cluster_movies']
        recommendations = list(map(lambda x: x['id'], recommendation_data))
        recommendations.remove(movie_id)


        args = movie_recom_req_parser.parse_args()
        limit = args.get('limit')
        if limit is None:
            limit = len(recommendations)
        limited_recom = recommendations[:limit]
        return {
                'movie_id' : movie_id,
                'movie' : movie,
                'num_recommendations' : len(limited_recom),
                'recommendations': get_movies_info(limited_recom)
            }

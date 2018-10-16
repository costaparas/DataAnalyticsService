import random

from flask_restplus import Resource, Namespace, reqparse

from resources.movie import get_movies_info, build_movielist_response
from .requires_auth import requires_auth

api = Namespace("random", description="Get a random movie or sample of random movies.")
movie_list_req_parser = reqparse.RequestParser()
movie_list_req_parser.add_argument('limit', type=int, help="Limit number of results.", default=10)


@api.route('/movies')
class MovieList(Resource):
    @api.response(200, 'Success.')
    @api.doc(description="Get a random sample of movies.")
    @api.expect(movie_list_req_parser)
    @requires_auth(api)
    def get(self):
        args = movie_list_req_parser.parse_args()
        limit = args.get('limit')
        movie_data_list = get_movies_info([])
        if limit is None:
            limit = len(movie_data_list)
        shuffled = movie_data_list
        random.shuffle(shuffled)
        return build_movielist_response(movies=shuffled, limit=limit)
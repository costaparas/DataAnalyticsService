from flask_restplus import abort, Resource, Namespace, reqparse
from .requires_auth import requires_auth
from movie_data import get_movie_data

api = Namespace("random", description="Get a random selection of movies.")
movie_list_req_parser = reqparse.RequestParser()
movie_list_req_parser.add_argument('limit', type=int, help="Limit number of results.")
@api.route('/movies')
class MovieList(Resource):
    @api.response(200, 'Success.')
    @api.doc(description="Get a random selection of movies.")
    @api.expect(movie_list_req_parser)
    @requires_auth(api)
    def get(self):
        args = movie_list_req_parser.parse_args()
        limit = args.get('limit')
        movie_data_list = get_movies_info([])
        if limit is None:
            limit = len(movie_data_list)
        return {
            'movies': movie_data_list[:limit],
            'num_movies': limit
        }

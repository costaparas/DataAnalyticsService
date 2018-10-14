from flask_restplus import abort, Resource, Namespace, reqparse
from .requires_auth import requires_auth
from movie_data import get_movie_data

api = Namespace("movies", description="Movie data.")

def get_movie_or_404(movie_id):
    movie_data = get_movie_data()
    if movie_id in movie_data:
        return movie_data[movie_id]
    else:
        abort(404, "Movie not found.")

def get_movies_info(movie_ids):
    movie_data_dict = get_movie_data()
    movie_data_list = []
    for movie_id, movie_obj in movie_data_dict.items():
        if movie_ids and not movie_id in movie_ids: continue
        new_movie_obj = movie_obj.copy()
        new_movie_obj['movie_id'] = movie_id
        movie_data_list.append(new_movie_obj)
    return movie_data_list

@api.param("movie_id", "Movie ID")
@api.route('/<string:movie_id>')
class Movie(Resource):
    @api.response(200, 'Movie found.')
    @api.response(404, 'Movie not found.')
    @api.doc(description="Get information about a particular movie.")
    @requires_auth(api)
    def get(self, movie_id):
        return get_movie_or_404(movie_id)


movie_list_req_parser = reqparse.RequestParser()
movie_list_req_parser.add_argument('limit', type=int, help="Limit number of results.")
@api.route('')
class MovieList(Resource):
    @api.response(200, 'Success.')
    @api.doc(description="Get a list of available movies.")
    @api.expect(movie_list_req_parser)
    @requires_auth(api)
    def get(self):
        args = movie_list_req_parser.parse_args()
        limit = args.get('limit')
        movie_data_list = get_movies_info()
        if limit is None:
            limit = len(movie_data_list)
        return {
            'movies': movie_data_list[:limit],
            'num_movies': limit
        }

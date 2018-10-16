from flask_restplus import abort, Resource, Namespace, reqparse

from movie_data import get_movie_data
from .requires_auth import requires_auth
from resources.utils import release_date_to_datetime
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
        if len(movie_ids) > 1 and not movie_id in movie_ids: continue
        if movie_obj["Title"] == '#DUPE#': continue
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
movie_list_req_parser.add_argument('inTitle', type=str, help="Query movies by title.")

SORT_BY_RELEASE_DATE_ASC = "release-date-oldest"
SORT_BY_RELEASE_DATE_DESC = "release-date-newest"
SORT_BY_TITLE = "title"

movie_list_req_parser.add_argument('sortBy', choices=(SORT_BY_RELEASE_DATE_ASC, SORT_BY_RELEASE_DATE_DESC, SORT_BY_TITLE), help="Sort search results.",
                                   default=SORT_BY_TITLE)


@api.route('')
class MovieList(Resource):
    @api.response(200, 'Success.')
    @api.doc(description="Get a list of available movies.")
    @api.expect(movie_list_req_parser)
    @requires_auth(api)
    def get(self):
        args = movie_list_req_parser.parse_args()
        limit = args.get('limit')
        inTitle = args.get("inTitle")
        if inTitle is None: inTitle = ""
        sortBy = args.get("sortBy")

        movie_data_list = get_movies_info([])
        filtered = [x for x in movie_data_list if inTitle in x["Title"].lower()]
        movie_data_list = filtered
        if sortBy == SORT_BY_TITLE:
            sorted_movies = list(sorted(movie_data_list, key=lambda x:x["Title"]))
            movie_data_list = sorted_movies
        elif sortBy in [SORT_BY_RELEASE_DATE_DESC,SORT_BY_RELEASE_DATE_ASC]:
            do_reversed = sortBy == SORT_BY_RELEASE_DATE_DESC
            sorted_movies = list(sorted(
                movie_data_list,
                key=lambda x:release_date_to_datetime(x["Released"]),
                reverse=do_reversed
            ))
            movie_data_list = sorted_movies
        else:
            pass
        if limit is None:
            limit = len(movie_data_list)
        return {
            'movies': movie_data_list[:limit],
            'num_movies': limit
        }

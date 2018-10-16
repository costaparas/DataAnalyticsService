from flask_restplus import Resource, Namespace

from movie_data import get_movie_data
from .requires_auth import requires_auth

api = Namespace("genres", description="List of available movie genres.")


def get_genres():
    movies = get_movie_data()
    all_genres = set()
    for _, movie in movies.items():
        if "Genre" in movie:
            genres = movie["Genre"].split(",")
            for genre in genres: all_genres.add(genre.strip())
    if "N/A" in all_genres:
        all_genres.remove("N/A")
    return list(all_genres)


@api.route('')
class GenreList(Resource):
    @api.response(200, 'Success.')
    @api.doc(description="Get a list of available movie genres.")
    @requires_auth(api)
    def get(self):
        genres = get_genres()
        sorted_ = list(sorted(genres, key=lambda x:x))
        return {
            "genres": sorted_,
        }

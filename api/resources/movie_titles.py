from flask_restplus import Resource, Namespace

# from movie_data import get_movie_data
from resources.movie import get_movies_info
from .requires_auth import requires_auth

api = Namespace("movie_titles", description="List of available movie titles.")


def get_movie_titles():
    movies = get_movies_info(movie_ids=[])
    titles = []
    for movie in movies:
        # Needed to return more information to distinguish
        # duplicate title movies to user.
        # E.g. There are 3 movies titled "Alice in Wonderland".
        titles.append({
            "movie_id" : movie["movie_id"],
            "title" : movie["Title"],
            "year" : movie["Year"],
            "poster" : movie["Poster"],
            # "released" : movie["Released"],
        })
    sorted_titles = list(sorted(titles, key=lambda x:x["title"]))
    return sorted_titles


@api.route('')
class MovieTitleList(Resource):
    @api.response(200, 'Success.')
    @api.doc(description="List of available movie titles.")
    @requires_auth(api)
    def get(self):
        titles = get_movie_titles()
        return {
            "movies": titles,
            "num_movies" : len(titles)
        }

from flask_restplus import Resource, abort

from movie_data import get_movie_data

def get_movie_or_404(movie_id):
    movie_data = get_movie_data()
    if movie_id in movie_data:
        return movie_data[movie_id]
    else:
        abort(404, "Movie not found.")

class Movie(Resource):
    def get(self, movie_id):
        return get_movie_or_404(movie_id)


class MovieList(Resource):
    def get(self):
        movie_data = get_movie_data()
        movie_ids = list(movie_data.keys())
        return {
            'movies': movie_ids,
            'num_movies': len(movie_ids)
        }


class Recommendations(Resource):
    def get(self, movie_id):
        movie = get_movie_or_404(movie_id)
        return {
                'movie_id' : movie_id,
                'movie' : movie,
                'recommendations': []
            }

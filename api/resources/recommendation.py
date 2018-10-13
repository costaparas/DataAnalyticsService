from flask_restplus import Resource

from resources.movie import get_movie_or_404


class Recommendations(Resource):
    def get(self, movie_id):
        movie = get_movie_or_404(movie_id)
        return {
                'movie_id' : movie_id,
                'movie' : movie,
                'recommendations': []
            }
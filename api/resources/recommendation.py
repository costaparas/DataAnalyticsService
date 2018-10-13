from flask_restplus import Resource, Namespace

from resources.movie import get_movie_or_404


api = Namespace("recommendations", description="")

@api.route('/<string:movie_id>')
class Recommendations(Resource):
    def get(self, movie_id):
        movie = get_movie_or_404(movie_id)
        return {
                'movie_id' : movie_id,
                'movie' : movie,
                'recommendations': []
            }
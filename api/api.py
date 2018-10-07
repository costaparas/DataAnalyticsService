from flask import Flask
from flask_restplus import Api, Resource

app = Flask(__name__)
api = Api(app,
          # default="Movies",
          # default_label="Movies and recommendations.",
          title="Movie Recommendation API",
          description="This API provides access to a database of movie titles, information about each title and movie recommendations.",
          version="1.0"
          )
api.namespaces.clear()
movies_ns = api.namespace("movies", description="")
recommendations_ns = api.namespace("recommendations", description="")

@movies_ns.route('/list')
class Movies(Resource):
    def get(self):
        return {'movies': []}

@recommendations_ns.route('/<string:movie_id>')
class Recommendations(Resource):
    def get(self, movie_id):
        return {'recommendations': []}
if __name__ == '__main__':
    app.run(debug=True)
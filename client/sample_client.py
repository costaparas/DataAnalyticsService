import flask
from flask import Flask
from jinja2 import Template

from api_client import ApiClient

CONFIG_API_CLIENT = "api client"
app = Flask(__name__)
app.config[CONFIG_API_CLIENT] = ApiClient(
    server_url="https://movie-recommender-api.herokuapp.com"
)


def get_api_client():
    return flask.current_app.config[CONFIG_API_CLIENT]


@app.route('/', methods=['GET'])
def home_page():
    movies = get_api_client().get_movies(limit=5)
    template = """
    <html>
    <ul>
    {% for m in movies %}
        {% if "Poster" in m %}
            <li><img style="height:200px" src='{{m["Poster"]}}'/></li>
        {% endif %}
    {% endfor %}
    </ul>
    </html>
    """
    #Don't actually do this... use flask.render_template()
    return Template(template).render(movies=movies)


if __name__ == '__main__':
    app.run(debug=True)

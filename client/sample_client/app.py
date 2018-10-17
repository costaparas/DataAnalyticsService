from flask import Flask
from client.api_client import ApiClient
CONFIG_API_CLIENT = "api client"
app = Flask(__name__)
app.config[CONFIG_API_CLIENT] = ApiClient(
    server_url="https://movie-recommender-api.herokuapp.com/"
)


@app.route('/', methods=['GET', 'POST'])
def home_page():
    return ""

if __name__ == '__main__':
    app.run(debug=True)

FILE SUMMARY
============

* `main.py`: entry-point for the client application
* `api_client/`: an interface for making requests to the API
* `templates/`: Jinja2 template files for the client application
* `static/`: image and CSS resources used by the client application
* `README.md`: this file

CLIENT USAGE
============

* By default, the client is run on port 5000 and uses
the deployed API at <https://movie-recommender-api.herokuapp.com>
* The following examples show how to change the default execution

```sh
# Run client on default port 5000
python3 main.py

# Run client with specifed port number $PORT
python3 main.py --port $PORT

# Run client with specifed custom API $URL
python3 main.py --api_url "$URL"

# Run client with specifed port number $PORT and custom API $URL
python3 main.py --port $PORT --api_url "$URL"
```

COPYRIGHT INFORMATION
=====================

* Some images used in this site are borrowed from online sources.
* It is not our intention to commit copyright infringement.
* We also acknowledge the use of Materialize CSS, for more information see
<https://github.com/costaparas/DataAnalyticsService/blob/master/client/static/assets/materialize/README.md>

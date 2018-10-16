# DataAnalyticsService
A RESTful API for recommending movies to users

## Description
This service provides a fast, reliable means for users to find movies they may be interested in watching. The service provides a RESTful API for movie recommendation, as well as a client program for ease of user browsing. The recommender system is build on Python 3 using machine learning algorithms provided by the Scikit-learn (<http://scikit-learn.org/stable/>) library.

## Getting Started

### Prerequisites
It is assumed that:
* Python 3.6.5 or above is installed (<https://www.python.org/downloads/>)
* Heroku CLI 7.16.8 is installed (<https://devcenter.heroku.com/articles/heroku-cli#download-and-install>)

### Installation
`pip3 install -r requirements.txt`

## Usage
Refer to README.md files in the individual project directories for details

## Deployment
The API and client application are deployed in separate instances on the Heroku cloud platform as a service:
* API is hosted at: <https://movie-recommender-api.herokuapp.com/>

### Heroku Configuration
```sh
# Login to Heroku CLI
heroku login

# Ensure you are listed as a collaborator:
# https://dashboard.heroku.com/apps/movie-recommender-api/access

# Add the heroku remote
heroku git:remote -a movie-recommender-api

# Set the private key for use by the API
heroku config:set PRIVATE_KEY=`python3 api/generate_private_key.py /tmp/.private_key`
```

### Deploy API
```sh
# Deploy from master branch
git push heroku master

# Deploy from branch 'foo'
git push heroku foo:master

# Restart the server if needed
heroku restart

# View the server logs
heroku logs --tail
```

## Project Structure
* `ml/` - backend Machine Learning algorithms consumed by API
* `api/` - RESTful API based on Flask-RESTPlus
* `client/` - client GUI for the API built on Flask and Materialize
* `data/` - datasets used by ML algorithms

## Contributing
1. Clone the repository (`git clone git@github.com:costaparas/DataAnalyticsService.git`)
2. Create a new feature branch (`git checkout -b foobar-feature`)
3. Commit new changes (`git commit -a -m 'add foobar'`)
4. Push to the branch (`git push origin foobar-feature`)
5. Create a new Pull Request (<https://github.com/costaparas/DataAnalyticsService/pulls>)
6. Merge the Pull Request once it is approved by at least one other contributor

## License
Copyright (C) 2018 Benjamin Liew, Costa Paraskevopoulos, Dankoon Yoo, Saffat Akanda, Sharon Park

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.

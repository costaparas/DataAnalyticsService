from flask_restplus import (
    Resource, reqparse,
    Namespace,abort )
from flask import current_app
TEST_USERS = {
    # username : password
    "user": "test1",
}

api = Namespace("token", description="")
credential_parser = reqparse.RequestParser()
credential_parser.add_argument('username', type=str)
credential_parser.add_argument('password', type=str)


@api.route('/generate')
class GenerateToken(Resource):

    @api.expect(credential_parser, validate=True)
    def get(self):
        args = credential_parser.parse_args()
        username = args.get('username')
        password = args.get('password')
        if username in TEST_USERS and TEST_USERS[username] == password:

            auth = current_app.config.get(AUTH_FACTORY)
            return {"token" : None}
        else:
            abort(401,"Bad username and/or password.")


@api.route('/validate')
class ValidateToken(Resource):
    def get(self):
        return {}

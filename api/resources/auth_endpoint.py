from ago import human
from datetime import datetime
from flask_restplus import (
    Resource, reqparse,
    Namespace, abort)
from itsdangerous import BadSignature, SignatureExpired

from .app_context import get_auth

TEST_USERS = {
    # username : password
    "user": "test1",
}

api = Namespace("token", description="API authentication token.")
credential_parser = reqparse.RequestParser()
credential_parser.add_argument('username', type=str, required=True, location="form")
credential_parser.add_argument('password', type=str, required=True, location="form")


@api.route('/generate')
class GenerateToken(Resource):

    @api.expect(credential_parser, validate=True)
    @api.response(201, 'API token created.')
    @api.response(401, 'Unauthorized: bad credentials.')
    @api.doc(description="Generate an API token from credentials.")
    def post(self):
        args = credential_parser.parse_args()
        username = args.get('username')
        password = args.get('password')
        if username in TEST_USERS and TEST_USERS[username] == password:
            token = get_auth().generate(username=username)
            return {"token": token}, 201
        else:
            abort(401)


token_parser = reqparse.RequestParser()
token_parser.add_argument('token', type=str, required=True, location="form")


@api.route('/validate')
class ValidateToken(Resource):
    @api.expect(token_parser, validate=True)
    @api.response(200, 'Token given.')
    @api.response(400, 'No token given.')
    @api.doc(description="Validate an API token.")
    def post(self):
        args = token_parser.parse_args()
        token = args.get('token')
        if token is None: abort(400)
        try:
            token_payload = get_auth().validate(token)
            exp_epoch = token_payload['exp']
            utc = datetime.utcfromtimestamp(exp_epoch)
            iso = utc.isoformat() + "Z"
            delta = datetime.utcnow() - utc
            return {
                    "token_status": "valid",
                    "expires_at": iso,
                    "expires_in_roughly": human(delta, future_tense="{0}")
                    }
        except (BadSignature, SignatureExpired):
            return {
                "token_status": "invalid"
            }

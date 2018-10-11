import pytest
from auth import AuthTokenFactory

def test_auth_token():
    SECRET_KEY = "ahslkjdf234ulwken"
    auth = AuthTokenFactory(secret_key=SECRET_KEY)
    token = auth.generate(username="bob")
    auth.validate(token)

if __name__ == '__main__':
    pytest.main([])

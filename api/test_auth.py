import pytest
from auth import AuthTokenFactory

def test_auth_token():
    auth = AuthTokenFactory(secret_key="thisisasecret!")
    pass

if __name__ == '__main__':
    pytest.main([])

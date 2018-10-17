import requests

class ApiClient:
    def __init__(self,server_url,token=None):
        self.server_url = server_url
        if token is None:
            self.token = self.get_new_token()
        else:
            self.token = token

    def get_new_token(self):
        pass


    def validate_own_token(self):
        pass

    @staticmethod
    def validate_token(token):
        pass


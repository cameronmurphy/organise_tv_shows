import requests
import sys


class PushoverClient:
    API_OP_SEND = 'https://api.pushover.net/1/messages.json'

    def __init__(self, api_token, api_user_key, device_name=None):
        self.api_token = api_token
        self.api_user_key = api_user_key
        self.device_name = device_name

    def send(self, message):
        pushover_params = {'token': self.api_token, 'user': self.api_user_key, 'message': message}

        if self.device_name is not None:
            pushover_params['device'] = self.device_name

        response = requests.post(self.API_OP_SEND, pushover_params)

        if response.status_code != 200:
            sys.stderr.write(
                f'api.pushover.net returned {response.status_code}, content: {response.content}\n'
            )

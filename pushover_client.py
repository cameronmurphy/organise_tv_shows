import requests
import sys


class PushoverClient:
    API_OP_SEND = 'https://api.pushover.net/1/messages.json'

    def __init__(self, api_token, api_user_key):
        self.api_token = api_token
        self.api_user_key = api_user_key

    def send(self, message, device_name=None):
        pushover_params = {'token': self.api_token, 'user': self.api_user_key, 'message': message}

        if device_name is not None:
            pushover_params['device'] = device_name

        response = requests.post(self.API_OP_SEND, pushover_params)

        if response.status_code != 200:
            sys.stderr.write(
                'api.pushover.net returned {0}, content: {1}\n'.format(response.status_code, response.content)
            )

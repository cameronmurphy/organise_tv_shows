import requests


class TVDBClient:
    DOMAIN = 'https://api.thetvdb.com'
    OP_LOGIN = DOMAIN + '/login'
    OP_SEARCH_SERIES = DOMAIN + '/search/series'
    OP_GET_EPISODES = DOMAIN + '/series/{0}/episodes/query'

    def __init__(self, api_key, user_key, username):
        self.api_key = api_key
        self.user_key = user_key
        self.username = username
        self.token = None

    @staticmethod
    def __sanitize(string):
        # Handle unicode RIGHT SINGLE QUOTATION MARK
        string = string.replace(u'\u2019', u'\'')
        # Support all file systems, no slashes
        string = string.replace('/', ' + ')
        # Support Windows filesystem (no ? or :)
        string = string.replace(': ', ' - ').replace(':', '.').replace('?', '')
        string = string.strip()
        return string

    def __authenticated_get_request(self, url, params):
        if self.token is None:
            raise RuntimeError('Cannot perform request, TVDB not logged in')

        response = requests.get(url, params=params, headers={'Authorization': 'Bearer {0}'.format(self.token)})

        if response.status_code != 200:
            return None

        try:
            json = response.json()
        except ValueError:
            return None

        return json

    def login(self):
        response = requests.post(self.OP_LOGIN, json={
            'apikey': self.api_key,
            'userkey': self.user_key,
            'username': self.username
        })

        if response.status_code != 200:
            raise RuntimeError('Could not login to TVDB API, status: {0}, error: {1}'.format(
                response.status_code,
                response.json()
            ))

        response_decoded = response.json()

        if 'token' not in response_decoded or not len(response_decoded['token']) > 0:
            raise RuntimeError('TVDB API login response is missing token: {0}'.format(response_decoded))

        self.token = response_decoded['token']

    def get_series_info(self, series_name):
        response = self.__authenticated_get_request(self.OP_SEARCH_SERIES, {'name': series_name})

        if response is None:
            return None, None

        series_data = response['data'][0]
        return series_data['id'], self.__sanitize(series_data['seriesName'])

    def get_episode_title(self, series_id, season_index, episode_index):
        response = self.__authenticated_get_request(
            self.OP_GET_EPISODES.format(series_id),
            {'airedSeason': season_index, 'airedEpisode': episode_index}
        )

        if response is None:
            return None

        episode_data = response['data'][0]
        return self.__sanitize(episode_data['episodeName'])

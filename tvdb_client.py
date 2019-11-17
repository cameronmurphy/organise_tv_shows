import requests
import xml.etree.ElementTree as ElementTree


class TVDBClient:
    API_DOMAIN = 'https://thetvdb.com'
    API_OP_GET_SERIES = API_DOMAIN + '/api/GetSeries.php?seriesname='
    API_OP_GET_EPISODE = API_DOMAIN + '/api/{0}/series/{1}/default/{2}/{3}'
    API_SERIES_ID_XPATH = './Series/seriesid'
    API_SERIES_NAME_XPATH = './Series/SeriesName'
    API_EPISODE_NAME_XPATH = './Episode/EpisodeName'

    def __init__(self, api_key):
        self.api_key = api_key

    @staticmethod
    def sanitize(string):
        # Handle unicode RIGHT SINGLE QUOTATION MARK
        string = string.replace(u'\u2019', u'\'')
        # Support all file systems, no slashes
        string = string.replace('/', ' + ')
        # Support Windows filesystem (no ? or :)
        string = string.replace(': ', ' - ').replace(':', '.').replace('?', '')
        string = string.strip()
        return string

    def get_series_info(self, series_name):
        response = requests.get(self.API_OP_GET_SERIES + series_name.replace(' ', '%20'))

        if response.status_code != 200:
            return None, None

        root = ElementTree.fromstring(response.content)
        series_id_element = root.find(self.API_SERIES_ID_XPATH)
        series_name_element = root.find(self.API_SERIES_NAME_XPATH)

        if series_id_element is None or series_name_element is None:
            return None, None

        return series_id_element.text, self.sanitize(series_name_element.text)

    def get_episode_title(self, series_id, season_index, episode_index):
        response = requests.get(self.API_OP_GET_EPISODE.format(self.api_key, series_id, season_index, episode_index))

        if response.status_code != 200:
            return None

        root = ElementTree.fromstring(response.content)
        episode_name = root.find(self.API_EPISODE_NAME_XPATH).text

        return self.sanitize(episode_name)

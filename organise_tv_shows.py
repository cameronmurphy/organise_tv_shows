#!/usr/bin/env python3

import argparse
import os
import re
import hashlib
import shutil
import datetime
import requests
import yaml
import sys
import xml.etree.ElementTree as ElementTree
from config import validate_config

DEFAULT_PARAMETERS_FILENAME = 'organise_tv_shows.config.yml'


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


class MediaOrganiser:
    SRC_FILENAME_REGEX_SXXEXX = '([A-Za-z0-9\_\.\- ]+)[\._ ][Ss]([0-9]{1,2})[\._ \-]?[Ee]([0-9]{1,2})([^\\/]*)'
    SRC_FILENAME_REGEX_XxXX = '([A-Za-z0-9\_\.\- ]+)[\._ ]([0-9]{1,2})[\._ \-]?x([0-9]{1,2})([^\\/]*)'
    EPISODE_NAME_FORMAT = '{1} - {3}x{4:02d} - {5}{6}'
    DESTINATION_PATH_FORMAT = '{0}/{1}{2}/Season {3}/' + EPISODE_NAME_FORMAT

    def __init__(
        self,
        complete_downloads_path,
        library_path,
        tvdb_client,
        series_title_overrides=None,
        series_season_offsets=None,
        md5_check=False,
        pushover_client=None,
        pushover_device=None,
        pushover_ignore_hd=False
    ):
        self.complete_downloads_path = self.strip_trailing_slash(complete_downloads_path)
        self.library_path = self.strip_trailing_slash(library_path)
        self.tvdb_client = tvdb_client
        self.series_title_overrides = series_title_overrides
        self.series_season_offsets = series_season_offsets
        self.md5_check = md5_check
        self.pushover_client = pushover_client
        self.pushover_device = pushover_device
        self.pushover_ignore_hd = pushover_ignore_hd

    @staticmethod
    def strip_trailing_slash(path):
        if path.endswith('/'):
            path = path[:-1]

        return path

    @staticmethod
    def md5_for_file(path, block_size=256*128):
        md5 = hashlib.md5()

        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(block_size), b''):
                md5.update(chunk)

        return md5.hexdigest()

    def apply_series_season_offsets(self, series_id, season_index, episode_index):
        if self.series_season_offsets is not None:
            for entry in self.series_season_offsets:
                if entry['series_id'] == int(series_id) and int(season_index) >= entry['since_season_index']:
                    if entry['since_season_index'] == int(season_index):
                        if int(episode_index) > entry['since_episode_index']:
                            episode_index -= int(entry['since_episode_index'])
                            season_index += 1
                    else:
                        season_index += 1

        return season_index, episode_index

    def massage_series_name(self, series_name):
        if self.series_title_overrides is not None:
            for override in self.series_title_overrides:
                if series_name.lower() == override['match']:
                    return override['replacement']

        return series_name

    def process(self):
        for filename in os.listdir(self.complete_downloads_path):
            full_path = '{0}/{1}'.format(self.complete_downloads_path, filename)

            if os.path.isfile(full_path) and not filename.startswith('.'):
                filename_without_extension, extension = os.path.splitext(filename)

                if self.md5_check:
                    if extension != '.md5':
                        continue

                    with open(full_path, 'r') as md5_file:
                        md5_hash = md5_file.read().lower().strip()

                    # Strip .md5 extension
                    full_path = full_path[:-4]

                    if self.md5_for_file(full_path) != md5_hash:
                        continue

                    filename_without_extension, extension = os.path.splitext(filename_without_extension)

                match = re.search(self.SRC_FILENAME_REGEX_SXXEXX, filename_without_extension)

                if match is None:
                    match = re.search(self.SRC_FILENAME_REGEX_XxXX, filename_without_extension)

                if match is None:
                    sys.stderr.write('{0}: Could not match {1}\n'.format(datetime.datetime.now(), filename))
                    continue

                hd_filename_part = ''

                if re.search('1080p', filename_without_extension, re.I) is not None:
                    hd_filename_part = ' 1080p'
                elif re.search('720p', filename_without_extension, re.I) is not None:
                    hd_filename_part = ' 720p'

                current_series_name = self.massage_series_name(str(match.group(1)).replace('.', ' ').title())
                current_series_id, current_series_name = self.tvdb_client.get_series_info(current_series_name)

                if current_series_id is None:
                    sys.stderr.write(
                        '{0}: Series not found for {1}'.format(datetime.datetime.now(), filename_without_extension)
                    )
                    continue

                current_season_index, current_episode_index = self.apply_series_season_offsets(
                    current_series_id,
                    int(match.group(2)),
                    int(match.group(3))
                )

                current_episode_title = self.tvdb_client.get_episode_title(
                    current_series_id,
                    current_season_index,
                    current_episode_index
                )

                if current_episode_title is None:
                    sys.stderr.write(
                        '{0}: Episode not found for {1}\n'.format(datetime.datetime.now(), filename_without_extension)
                    )
                    continue

                destination = self.DESTINATION_PATH_FORMAT.format(
                    self.library_path,
                    current_series_name,
                    hd_filename_part,
                    current_season_index,
                    current_episode_index,
                    current_episode_title,
                    extension
                )

                if not os.path.exists(os.path.dirname(destination)):
                    os.makedirs(os.path.dirname(destination))

                shutil.move(full_path, destination)
                sys.stdout.write('{0}: Moved {1} to {2}\n'.format(datetime.datetime.now(), filename, destination))

                if self.md5_check and os.path.isfile(full_path + '.md5'):
                    os.remove(full_path + '.md5')

                current_episode_name = self.EPISODE_NAME_FORMAT.format(
                    None,
                    current_series_name,
                    hd_filename_part,
                    current_season_index,
                    current_episode_index,
                    current_episode_title,
                    ''
                )

                if self.pushover_client is not None and (not self.pushover_ignore_hd or len(hd_filename_part) == 0):
                    self.pushover_client.send(current_episode_name, self.pushover_device)


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        '--config-file',
        help='config file location (if not %s)' % DEFAULT_PARAMETERS_FILENAME
    )

    args = arg_parser.parse_args()
    config_file_location = args.config_file if (args.config_file is not None) else DEFAULT_PARAMETERS_FILENAME

    if len(config_file_location) == 0:
        raise RuntimeError('--config-file option must not be empty')

    # Only prepend script path when config file is not an absolute path
    if config_file_location[0] != '/':
        script_path = os.path.dirname(os.path.realpath(__file__))
        config_file_location = '%s/%s' % (script_path, config_file_location)

    config_document = yaml.load(open(config_file_location, 'r'))
    parameters = validate_config(config_document, os.path.basename(config_file_location))
    pushover_client = None

    if parameters['pushover'] is not None:
        pushover_client = PushoverClient(parameters['pushover']['token'], parameters['pushover']['user_key'])

    organiser = MediaOrganiser(
        parameters['complete_downloads_path'],
        parameters['library_path'],
        TVDBClient(parameters['tvdb_api_key']),
        parameters['series_title_overrides'],
        parameters['series_season_offsets'],
        parameters['md5_check'],
        pushover_client,
        parameters['pushover']['device']
        if parameters['pushover'] is not None and 'device' in parameters['pushover'] else None,
        parameters['pushover']['ignore_hd']
        if parameters['pushover'] is not None and 'ignore_hd' in parameters['pushover'] else False
    )

    organiser.process()

if __name__ == '__main__':
    main()

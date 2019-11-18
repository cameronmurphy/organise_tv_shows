#!/usr/bin/env python3

import argparse
import os
import yaml
from config import validate_config
from meda_organiser import MediaOrganiser
from pushover_client import PushoverClient
from tvdb_client import TVDBClient

DEFAULT_CONFIG_FILENAME = 'config.yml'


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        '--config-file',
        help='config file location (if not %s)' % DEFAULT_CONFIG_FILENAME
    )

    args = arg_parser.parse_args()
    config_file_location = args.config_file if (args.config_file is not None) else DEFAULT_CONFIG_FILENAME

    if len(config_file_location) == 0:
        raise RuntimeError('--config-file option must not be empty')

    # Only prepend script path when config file is not an absolute path
    if config_file_location[0] != '/':
        script_path = os.path.dirname(os.path.realpath(__file__))
        config_file_location = '%s/%s' % (script_path, config_file_location)

    config_document = yaml.load(open(config_file_location, 'r'), Loader=yaml.FullLoader)
    parameters = validate_config(config_document, os.path.basename(config_file_location))

    tvdb_client = TVDBClient(
        parameters['tvdb']['api_key'],
        parameters['tvdb']['user_key'],
        parameters['tvdb']['username']
    )
    tvdb_client.login()

    pushover_client = None

    if parameters['pushover'] is not None:
        pushover_client = PushoverClient(parameters['pushover']['token'], parameters['pushover']['user_key'])

    organiser = MediaOrganiser(
        parameters['complete_downloads_path'],
        parameters['library_path'],
        tvdb_client,
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

import argparse
import os

DEFAULT_CONFIG_FILENAME = 'config.yml'


def get_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        '--config-file',
        default=DEFAULT_CONFIG_FILENAME,
        help=f'config file location (if not {DEFAULT_CONFIG_FILENAME})'
    )

    args = arg_parser.parse_args()
    config_file = args.config_file

    if not config_file:
        raise argparse.ArgumentTypeError('--config-file option must not be empty')

    # Support relative paths
    if not os.path.isabs(config_file):
        config_file = os.path.join(os.path.dirname(os.path.realpath(__file__ + '/..')), config_file)

    return {'config_file': config_file}

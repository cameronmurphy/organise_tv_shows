import tvdb_v4_official
from organise_tv_shows.args import get_args
from organise_tv_shows.clients.pushover_client import PushoverClient
from organise_tv_shows.config import load_config
from organise_tv_shows.processor.processor import Processor


def main():
    args = get_args()
    config = load_config(args['config_file'])

    tvdb_client = tvdb_v4_official.TVDB(config.tvdb.api_key)
    pushover_client = None

    if config.pushover is not None:
        pushover_client = PushoverClient(config.pushover.token, config.pushover.user_key)

    processor = Processor(
        config,
        tvdb_client,
        pushover_client,
    )

    processor.process()

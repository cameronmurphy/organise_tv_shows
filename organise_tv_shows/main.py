from organise_tv_shows.args import get_args
from organise_tv_shows.config import load_config
from organise_tv_shows.processor.processor import Processor


def main():
    args = get_args()
    config = load_config(args['config_file'])

    processor = Processor(config)
    processor.process()

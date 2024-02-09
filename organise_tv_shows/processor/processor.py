import os
from typing import List

from organise_tv_shows.config import Config
from organise_tv_shows.processor.media import Media
from organise_tv_shows.processor.steps.filename_step import FilenameStep
from organise_tv_shows.processor.steps.load_series_config_step import LoadSeriesConfigStep
from organise_tv_shows.processor.steps.match_step import MatchStep
from organise_tv_shows.processor.steps.md5_cleanup_step import Md5CleanupStep
from organise_tv_shows.processor.steps.md5_step import Md5Step
from organise_tv_shows.processor.steps.organise_step import OrganiseStep
from organise_tv_shows.processor.steps.pushover_step import PushoverStep
from organise_tv_shows.processor.steps.resolve_step import ResolveStep
from organise_tv_shows.processor.steps.step import Step


class Processor:
    __STEPS: List[Step] = [
        FilenameStep(),
        Md5Step(),
        MatchStep(),
        LoadSeriesConfigStep(),
        ResolveStep(),
        OrganiseStep(),
        Md5CleanupStep(),
        PushoverStep(),
    ]

    def __init__(
        self,
        config: Config,
    ):
        self.config = config

    def process(self):
        for filename in os.listdir(self.config.complete_downloads_path):
            path = os.path.join(self.config.complete_downloads_path, filename)
            media = Media(filename, path)

            for step in self.__STEPS:
                result = step.process(media, self.config)

                if not result:
                    break

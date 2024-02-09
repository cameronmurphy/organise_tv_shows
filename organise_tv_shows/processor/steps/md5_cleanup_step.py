import os

from organise_tv_shows.processor.steps.step import Step


class Md5CleanupStep(Step):
    def process(self, media, config) -> bool:
        if not config.md5_check:
            return True

        if os.path.isfile(media.path + '.md5'):
            os.remove(media.path + '.md5')

        return True

import os

from organise_tv_shows.processor.steps.step import Step


class HashCleanupStep(Step):
    def process(self, media, config) -> bool:
        if not config.hash_check:
            return True

        if os.path.isfile(media.path + '.hash'):
            os.remove(media.path + '.hash')

        return True

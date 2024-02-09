import os

from organise_tv_shows.processor.steps.step import Step


class FilenameStep(Step):
    def process(self, media, config) -> bool:
        # Must be a file, must not be hidden, must have an extension with 3 chars
        return os.path.isfile(media.path) and \
            not media.filename.startswith('.') and len(media.extension) == 4

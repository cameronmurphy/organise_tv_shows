from organise_tv_shows.clients.pushover_client import PushoverClient
from organise_tv_shows.config import Config
from organise_tv_shows.processor.media import Media
from organise_tv_shows.processor.steps.step import Step


class PushoverStep(Step):
    def process(self, media: Media, config: Config) -> bool:
        if not config.pushover:
            return True

        client = PushoverClient(config.pushover.token, config.pushover.user_key, config.pushover.device)
        client.send(media.organised_filename_without_extension)

        return True

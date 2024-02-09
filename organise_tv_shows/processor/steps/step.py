from abc import ABC, abstractmethod

from organise_tv_shows.config import Config
from organise_tv_shows.processor.media import Media


class Step(ABC):
    # Returns true if processing should continue, false if processing of this media should stop.
    @abstractmethod
    def process(self, media: Media, config: Config) -> bool:
        pass

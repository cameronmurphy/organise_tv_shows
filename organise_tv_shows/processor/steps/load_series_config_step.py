from organise_tv_shows.config import Config, SeriesConfig
from organise_tv_shows.processor.media import Media
from organise_tv_shows.processor.steps.step import Step


class LoadSeriesConfigStep(Step):
    @staticmethod
    def __match(media: Media, series_config: SeriesConfig) -> bool:
        return series_config.name.lower() == media.parsed_series_name.lower() or \
            any(media.parsed_series_name.lower() == alias.lower()
                for alias in (series_config.aliases or []))

    def process(self, media: Media, config: Config) -> bool:
        for series_config in (config.series_config or []):
            if self.__match(media, series_config):
                media.set_series_config(series_config)
                break

        # We couldn't find series config, just use the parsed series name
        if not media.series_config:
            media.set_series_name(media.parsed_series_name.title())

        return True

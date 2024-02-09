import re
import sys
from datetime import datetime

from organise_tv_shows.clients.tvdb_client_ext import TVDBExt
from organise_tv_shows.processor.media import Media
from organise_tv_shows.processor.steps.step import Step


class ResolveStep(Step):
    tvdb_client: TVDBExt = None

    @staticmethod
    def __strip_special_chars(string):
        return re.sub('[^A-Za-z0-9&]+', '', string)

    def __names_match(self, name_a: str, name_b: str) -> bool:
        return self.__strip_special_chars(name_a).lower() == self.__strip_special_chars(name_b).lower()

    def __find_exact_series_result(self, results, series_name):
        for series in results:
            if self.__names_match(series['name'], series_name) or \
                    any(
                        self.__names_match(alias, series_name)
                        for alias in (series['aliases'] if 'aliases' in series else [])
                    ):
                return series

            return None

    def __resolve_series(self, media):
        results = self.tvdb_client.search(media.series_name, type='series')
        result = self.__find_exact_series_result(results, media.series_name)

        if not result:
            ampersand_series_name = re.sub(rf'(?i)and', '&', media.series_name)
            result = self.__find_exact_series_result(results, ampersand_series_name)

        return result

    def __resolve_episode(self, series, media: Media):
        result = self.tvdb_client.get_series_episode(
            series['tvdb_id'],
            media.season_no,
            media.episode_no,
            'default' if media.series_config is None or media.series_config.season_type is None else
            str(media.series_config.season_type)
        )

        if not result:
            return None

        if len(result['episodes']) == 1:
            return result['episodes'][0]

        return None

    def process(self, media, config) -> bool:
        self.tvdb_client = TVDBExt(config.tvdb.api_key)
        series = self.__resolve_series(media)

        if not series:
            sys.stderr.write(
                f'{datetime.now()}: Could not resolve series \'{media.series_name}\', file \'{media.filename}\'\n'
            )
            return False

        media.set_series_name(series['name'])

        episode = self.__resolve_episode(series, media)

        if not episode:
            sys.stderr.write(
                f'{datetime.now()}: Could not resolve episode {media.episode_no}, season {media.season_no}, ' +
                f'series \'{media.series_name}\', file \'{media.filename}\'\n'
            )
            return False

        media.set_episode_name(episode['name'])

        return True

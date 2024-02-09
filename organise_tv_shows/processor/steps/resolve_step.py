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
        return re.sub('[^A-Za-z0-9]+', '', string)

    def __resolve_series(self, media):
        results = self.tvdb_client.search(media.series_name, type='series')

        # Find exactly matching result
        results = [
            series for series in results
            if self.__strip_special_chars(series['name']).lower() ==
            self.__strip_special_chars(media.series_name).lower()
        ]

        if len(results) != 1:
            return None

        return results[0]

    def __resolve_episode(self, series, media: Media):
        result = self.tvdb_client.get_series_episode(
            series['tvdb_id'],
            media.season_no,
            media.episode_no,
            str(media.series_config.season_type or 'default'),
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

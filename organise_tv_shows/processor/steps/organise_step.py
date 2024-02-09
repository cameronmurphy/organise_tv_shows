import os
import shutil
import sys
from datetime import datetime

from organise_tv_shows.processor.steps.step import Step


class OrganiseStep(Step):
    EPISODE_NAME_FORMAT = '{1} - {3}x{4:02d} - {5}{6}'
    DESTINATION_PATH_FORMAT = '{0}/{1}{2}/Season {3}/' + EPISODE_NAME_FORMAT

    @staticmethod
    def __sanitize_for_fs(string: str) -> str:
        # Handle unicode RIGHT SINGLE QUOTATION MARK
        string = string.replace(u'\u2019', u'\'')
        # Support all file systems, no slashes
        string = string.replace('/', ' + ')
        # Support Windows filesystem (no : or ?)
        string = string.replace(': ', ' - ').replace(':', '.').replace('?', '')
        string = string.strip()
        return string

    def process(self, media, config) -> bool:
        sanitised_series_name = self.__sanitize_for_fs(media.series_name)
        sanitised_episode_name = self.__sanitize_for_fs(media.episode_name)

        destination = self.DESTINATION_PATH_FORMAT.format(
            config.library_path,
            sanitised_series_name,
            f' {media.hd_res}' if media.hd_res else '',
            media.season_no,
            media.episode_no,
            sanitised_episode_name,
            media.extension
        )

        media.set_organised_path(destination)

        if not os.path.exists(os.path.dirname(destination)):
            os.makedirs(os.path.dirname(destination))

        shutil.move(media.path, destination)
        sys.stdout.write(f'{datetime.now()}: Moved {media.path} to {destination}\n')

        return True

    pass

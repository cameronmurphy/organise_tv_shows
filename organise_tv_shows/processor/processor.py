import hashlib
import os

from tvdb_v4_official import TVDB

from organise_tv_shows.clients.pushover_client import PushoverClient
from organise_tv_shows.config import Config
from organise_tv_shows.processor.media import Media
from organise_tv_shows.processor.steps.filename_step import FilenameStep
from organise_tv_shows.processor.steps.log_step import LogStep
from organise_tv_shows.processor.steps.match_step import MatchStep
from organise_tv_shows.processor.steps.md5_step import Md5Step


class Processor:
    STEPS = [
        FilenameStep(),
        Md5Step(),
        MatchStep(),
        LogStep()
    ]

    SRC_FILENAME_REGEX_SXXEXX = '([A-Za-z0-9\_\.\-\(\) ]*?)(?:[\._\- ]{1,3})[Ss]([0-9]{1,2})[Ee]([0-9]{1,3})(?:[^\\/]*)'
    SRC_FILENAME_REGEX_XxXX = '([A-Za-z0-9\_\.\-\(\) ]*?)(?:[\._\- ]{1,3})([0-9]{1,2})x([0-9]{1,3})(?:[^\\/]*)'
    EPISODE_NAME_FORMAT = '{1} - {3}x{4:02d} - {5}{6}'
    DESTINATION_PATH_FORMAT = '{0}/{1}{2}/Season {3}/' + EPISODE_NAME_FORMAT

    def __init__(
        self,
        config: Config,
        tvdb_client: TVDB,
        pushover_client: PushoverClient = None
    ):
        self.config = config
        self.tvdb_client = tvdb_client
        self.pushover_client = pushover_client

    @staticmethod
    def strip_trailing_slash(path):
        if path.endswith('/'):
            path = path[:-1]

        return path

    @staticmethod
    def md5_for_file(path, block_size=256*128):
        md5 = hashlib.md5()

        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(block_size), b''):
                md5.update(chunk)

        return md5.hexdigest()

    def process(self):
        for filename in os.listdir(self.config.complete_downloads_path):
            path = os.path.join(self.config.complete_downloads_path, filename)
            media = Media(filename, path)

            for step in self.STEPS:
                result = step.process(media, self.config)

                if not result:
                    break

            #     match = re.search(self.SRC_FILENAME_REGEX_SXXEXX, filename_without_extension)
            #
            #     if match is None:
            #         match = re.search(self.SRC_FILENAME_REGEX_XxXX, filename_without_extension)
            #
            #     if match is None:
            #         sys.stderr.write('{0}: Could not match {1}\n'.format(datetime.datetime.now(), filename))
            #         continue
            #
            #     hd_res_match = re.search(r'(2160p|1080p|720p)', filename_without_extension, re.I)
            #     hd_res = f' {hd_res_match.group(0)}' if hd_res_match else ''
            #
            #     current_series_name = self.massage_series_name(str(match.group(1)).replace('.', ' ').title())
            #     current_series_id, current_series_name = self.tvdb_client.get_series_info(current_series_name)
            #
            #     if current_series_id is None:
            #         sys.stderr.write(
            #             '{0}: Series not found for {1}'.format(datetime.datetime.now(), filename_without_extension)
            #         )
            #         continue
            #
            #     current_season_index, current_episode_index = self.apply_series_season_offsets(
            #         current_series_id,
            #         int(match.group(2)),
            #         int(match.group(3))
            #     )
            #
            #     current_episode_title = self.tvdb_client.get_episode_title(
            #         current_series_id,
            #         current_season_index,
            #         current_episode_index
            #     )
            #
            #     if current_episode_title is None:
            #         sys.stderr.write(
            #             '{0}: Episode not found for {1}\n'.format(datetime.datetime.now(), filename_without_extension)
            #         )
            #         continue
            #
            #     destination = self.DESTINATION_PATH_FORMAT.format(
            #         self.library_path,
            #         current_series_name,
            #         hd_res,
            #         current_season_index,
            #         current_episode_index,
            #         current_episode_title,
            #         extension
            #     )
            #
            #     if not os.path.exists(os.path.dirname(destination)):
            #         os.makedirs(os.path.dirname(destination))
            #
            #     shutil.move(path, destination)
            #     sys.stdout.write('{0}: Moved {1} to {2}\n'.format(datetime.datetime.now(), filename, destination))
            #
            #     if self.md5_check and os.path.isfile(path + '.md5'):
            #         os.remove(path + '.md5')
            #         pass
            #
            #     current_episode_name = self.EPISODE_NAME_FORMAT.format(
            #         None,
            #         current_series_name,
            #         hd_res,
            #         current_season_index,
            #         current_episode_index,
            #         current_episode_title,
            #         ''
            #     )
            #
            #     if self.pushover_client is not None:
            #         self.pushover_client.send(current_episode_name)

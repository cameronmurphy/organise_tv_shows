import os

from organise_tv_shows.config import SeriesConfig


class Media:
    def __init__(self, filename: str, path: str):
        self.filename: str = filename
        self.path: str = path
        self.filename_without_extension: str = None
        self.extension: str = None
        self.organised_filename: str = None
        self.organised_path: str = None
        self.organised_filename_without_extension: str = None
        self.parsed_series_name: str = None
        self.series_name: str = None
        self.episode_name: str = None
        self.hd_res: str = None
        self.season_no: int = None
        self.episode_no: int = None
        self.series_config: SeriesConfig = None

        self.__parse_filename(filename)

    @staticmethod
    def __prepare_parsed_series_name(parsed_series_name: str) -> str:
        # Words are often separated by periods in the filename
        return parsed_series_name.replace('.', ' ')

    def __parse_filename(self, filename):
        self.filename_without_extension, self.extension = os.path.splitext(filename)

    def set_series_config(self, series_config: SeriesConfig):
        self.series_config = series_config
        self.series_name = series_config.name.title()

    def set_parsed_series_name(self, parsed_series_name: str):
        self.parsed_series_name = self.__prepare_parsed_series_name(parsed_series_name)

    def set_series_name(self, series_name):
        self.series_name = series_name

    def set_episode_name(self, episode_name):
        self.episode_name = episode_name

    def set_hd_res(self, hd_res: str):
        self.hd_res = hd_res

    def set_season_no(self, season_no: int):
        self.season_no = season_no

    def set_episode_no(self, episode_no: int):
        self.episode_no = episode_no

    def set_organised_path(self, organised_path: str):
        self.organised_path = organised_path
        self.organised_filename = os.path.basename(organised_path)
        self.organised_filename_without_extension, _ = os.path.splitext(self.organised_filename)

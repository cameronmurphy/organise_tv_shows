import os


class Media:
    def __init__(self, filename, path):
        self.filename = filename
        self.filename_without_extension, self.extension = os.path.splitext(filename)
        self.path = path
        self.series_name = None
        self.hd_res = None
        self.season_no: int = None
        self.episode_no: int = None

    def set_series_name(self, series_name: str):
        self.series_name = series_name

    def set_hd_res(self, hd_res: str):
        self.hd_res = hd_res

    def set_season_no(self, season_no: int):
        self.season_no = season_no

    def set_episode_no(self, episode_no: int):
        self.episode_no = episode_no

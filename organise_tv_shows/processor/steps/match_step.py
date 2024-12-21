import re
import sys
from datetime import datetime
from organise_tv_shows.processor.steps.step import Step


class MatchStep(Step):
    FILENAME_REGEX_SXXEXX = '([A-Za-z0-9_.() !-]*?)(?:[._ -]{1,3})[Ss]([0-9]{1,2})[Ee]([0-9]{1,3})(?:[^\\/]*)'
    FILENAME_REGEX_XxXX = '([A-Za-z0-9_.() !-]*?)(?:[._ -]{1,3})([0-9]{1,2})x([0-9]{1,3})(?:[^\\/]*)'

    def process(self, media, config) -> bool:
        match = re.search(self.FILENAME_REGEX_SXXEXX, media.filename_without_extension)

        if match is None:
            match = re.search(self.FILENAME_REGEX_XxXX, media.filename_without_extension)

        if match is None:
            sys.stderr.write(f'{datetime.now()}: Could not match {media.filename}\n')
            return False

        media.set_parsed_series_name(match.group(1))
        media.set_season_no(int(match.group(2)))
        media.set_episode_no(int(match.group(3)))

        hd_res_match = re.search(r'(2160p|1080p|720p)', media.filename_without_extension, re.I)

        if hd_res_match:
            media.set_hd_res(hd_res_match.group(0))

        return True

from organise_tv_shows.processor.steps.step import Step


class LogStep(Step):
    def process(self, media, config) -> bool:
        print(media.series_name, media.season_no, media.episode_no, media.hd_res)
        return True

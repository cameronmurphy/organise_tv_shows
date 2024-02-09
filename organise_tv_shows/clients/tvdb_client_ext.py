from tvdb_v4_official import TVDB


class TVDBExt(TVDB):
    def get_series_episode(
            self,
            id: int,
            season: int,
            episode_number: int,
            season_type: str = "default",
            page: int = 0
    ) -> dict:
        url = self.url.construct(
            'series',
            id,
            'episodes/' + season_type,
            None,
            page=page,
            season=season,
            episodeNumber=episode_number
        )
        return self.request.make_request(url)

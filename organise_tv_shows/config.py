from typing import Optional, List
import yaml
from pydantic import BaseModel


class TVDBConfig(BaseModel):
    api_key: str


class PushoverConfig(BaseModel):
    token: str
    user_key: str
    device: Optional[str] = None
    ignore_hd: Optional[bool] = False


class SeriesTitleOverride(BaseModel):
    match: str
    replacement: str


class SeriesConfig(BaseModel):
    series_id: str
    since_season_index: int
    since_episode_index: int


class Config(BaseModel):
    complete_downloads_path: str
    library_path: str
    md5_check: Optional[bool] = False
    tvdb: TVDBConfig
    pushover: Optional[PushoverConfig] = None
    series_config: Optional[List[SeriesConfig]] = None


class Document(BaseModel):
    config: Config


def load_config(config_file_path) -> Config:
    config = yaml.load(open(config_file_path, 'r'), Loader=yaml.FullLoader)
    document = Document(**config)
    return document.config

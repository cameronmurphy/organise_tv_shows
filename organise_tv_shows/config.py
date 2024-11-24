from typing import Optional, List, Literal
import yaml
from pydantic import BaseModel


class TVDBConfig(BaseModel):
    api_key: str


class PushoverConfig(BaseModel):
    token: str
    user_key: str
    device: Optional[str] = None


class SeriesConfig(BaseModel):
    name: str
    season_type: Optional[Literal[
        'default',
        'official',
        'dvd',
        'absolute',
        'alternative',
        'regional'
    ]] = None
    aliases: Optional[List[str]] = None


class Config(BaseModel):
    complete_downloads_path: str
    library_path: str
    hash_check: Optional[bool] = False
    tvdb: TVDBConfig
    pushover: Optional[PushoverConfig] = None
    series_config: Optional[List[SeriesConfig]] = None


class Document(BaseModel):
    config: Config


def load_config(config_file_path) -> Config:
    config = yaml.load(open(config_file_path, 'r'), Loader=yaml.FullLoader)
    document = Document(**config)
    return document.config

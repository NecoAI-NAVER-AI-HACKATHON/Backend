import os
from typing import List

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from typing import Literal, Optional

load_dotenv()

ENV: str = os.getenv('ENV', 'dev')


class Configs(BaseSettings):
    ENV: str = os.getenv('ENV', 'dev')

    API: str = '/api'
    API_V1_STR: str = '/api/v1'
    API_V2_STR: str = '/api/v2'

    PROJECT_NAME: str = 'Neco AI'

    ENV_DATABASE_MAPPER: dict = {
        'prod': 'prod',
        'dev': 'dev',
        'test': 'test',
        'local': 'local',
    }
    DB_ENGINE_MAPPER: dict = {
        'postgresql': 'postgresql',
        'supabase': 'supabase',
    }

    PROJECT_ROOT: str = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )

    DATETIME_FORMAT: str = '%d-%m-%YT%H:%M:%S'
    DATE_FORMAT: str = '%d-%m-%Y'

    SECRET_KEY: str = os.getenv('SECRET_KEY', '')
    ACCESS_TOKEN_MAX_AGE: int = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 60 * 2)
    REFRESH_TOKEN_MAX_AGE: int = 2592000      # 30d
    COOKIE_SECURE: bool = False               # True in prod (HTTPS)
    COOKIE_SAMESITE: Literal["lax","strict","none"] = "lax"
    COOKIE_DOMAIN: Optional[str] = None       # e.g. .example.com
    COOKIE_PATH: str = "/"
    ACCESS_TOKEN_NAME: str = "access_token"
    REFRESH_TOKEN_NAME: str = "refresh_token"

    BACKEND_CORS_ORIGINS: List[str] = ['*']

    SUPABASE_URL: str = os.getenv('SUPABASE_URL', '')
    SUPABASE_ANON_KEY: str = os.getenv('SUPABASE_ANON_KEY', '')

    PAGE: int = 1
    PAGE_SIZE: int = 20
    ORDERING: str = '-id'

    class Config:
        case_sensitive = True


class TestConfigs(Configs):
    ENV: str = 'test'


configs = Configs()

if ENV == 'prod':
    pass
elif ENV == 'stage':
    pass
elif ENV == 'test':
    configs = TestConfigs()

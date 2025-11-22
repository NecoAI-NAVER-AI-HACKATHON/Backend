import os
from typing import List

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

ENV: str = os.getenv('ENV', 'dev')


class AppConfig(BaseSettings):
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
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 60 * 2)

    BACKEND_CORS_ORIGINS: List[str] = ['*']

    DB_USER: str = os.getenv('DB_USER', 'neco_ai_user')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD', 'neco_ai_password')
    DB_HOST: str = os.getenv('DB_HOST', 'localhost')
    DB_PORT: str = os.getenv('DB_PORT', '5432')
    DB_NAME: str = os.getenv('DB_NAME', 'neco_ai_db')
    DB_ENGINE: str = os.getenv('DB_ENGINE', 'postgresql')

    DATABASE_URI_FORMAT: str = (
        '{db_engine}://{user}:{password}@{host}:{port}/{database}'
    )

    DATABASE_URI: str = DATABASE_URI_FORMAT.format(
        db_engine=DB_ENGINE,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
    )

    SUPABASE_URL: str = os.getenv('SUPABASE_URL', '')
    SUPABASE_ANON_KEY: str = os.getenv('SUPABASE_ANON_KEY', '')

    REDIS_URL: str = os.getenv('REDIS_URL', 'redis://35.189.8.131:6379/1')
    MAIN_QUEUE: str = os.getenv('MAIN_QUEUE', 'queue:main')

    PAGE: int = 1
    PAGE_SIZE: int = 20
    ORDERING: str = '-id'

    class Config:
        case_sensitive = True


class TestConfig(AppConfig):
    ENV: str = 'test'


configs = AppConfig()

if ENV == 'prod':
    pass
elif ENV == 'stage':
    pass
elif ENV == 'test':
    configs = TestConfig()

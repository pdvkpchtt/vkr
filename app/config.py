from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal
from dotenv import find_dotenv

class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]

    dbname: str
    user: str
    password: str
    host: str
    port: int

    key: str
    algoritm: str

    smtp_host:str
    smtp_port:int
    smtp_user: str
    smtp_pass:str

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"

    model_config = SettingsConfigDict(env_file=find_dotenv("vkr/.env"))


settings = Settings()

# LOG_LEVEL: str
#
# test_dbname: str
# test_user: str
# test_password: str
# test_host: str
# test_port: int

# @property
# def DATABASE_URL_asyncpg_test(self):
#     return f"postgresql+asyncpg://{self.test_user}:{self.test_password}@{self.test_host}:{self.test_port}/{self.test_dbname}"

# smtp_host:str
# smtp_port:int
# smtp_user: str
# smtp_pass:str
#
# redis_host: str
# redis_port: str

# key: str
# algoritm: str
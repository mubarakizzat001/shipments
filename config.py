from pydantic_settings import SettingsConfigDict
from pydantic_settings import BaseSettings


class database_config(BaseSettings):
    postgres_server:str
    postgres_port:int
    postgres_user:str
    postgres_password:str
    postgres_db:str


    model_config = SettingsConfigDict(
        env_file="./.env",
        env_ignore_empty=True,
        extra="ignore"
    )

    @property
    def postgres_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_server}:{self.postgres_port}/{self.postgres_db}"

settings = database_config()


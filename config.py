from pydantic_settings import SettingsConfigDict
from pydantic_settings import BaseSettings




_base_config=SettingsConfigDict(
        env_file="./.env",
        env_ignore_empty=True,
        extra="ignore"
    )

class database_config(BaseSettings):
    postgres_server:str
    postgres_port:int
    postgres_user:str
    postgres_password:str
    postgres_db:str


    model_config=_base_config

    @property
    def postgres_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_server}:{self.postgres_port}/{self.postgres_db}"



class secret_key(BaseSettings):
    JWT_secret: str
    JWT_algorithm: str


    model_config=_base_config




settings = database_config()  
secret_settings=secret_key()

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    driver: str
    url: str
    host: str
    port: int

    @computed_field  # type: ignore[prop-decorator]
    @property
    def db_url(self) -> str:
        return f'{self.driver}:///{self.url}'

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()

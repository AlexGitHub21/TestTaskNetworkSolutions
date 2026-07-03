from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class DBSettings(BaseSettings):
    DB_NAME: str
    DB_ECHO: bool

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    # возвращаем строку подключения к бд
    @property
    def async_db_url(self):
        return f"sqlite+aiosqlite:///{self.DB_NAME}"

    @property
    def sync_db_url(self):
        return f"sqlite:///{self.DB_NAME}"


class Settings(BaseSettings):
    secret_key: SecretStr
    templates_dir: str = "app/templates"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


db_settings = DBSettings()
app_settings = Settings()
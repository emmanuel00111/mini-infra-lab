from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "mini-infra-lab"
    app_env: str = "dev"          # dev | prod
    log_level: str = "INFO"       # DEBUG | INFO | WARNING | ERROR
    include_timing: bool = True

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

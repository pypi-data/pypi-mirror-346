
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class BelinkPluginEnv(BaseSettings):
    MAX_REQUEST_TIMEOUT: int = Field(default=300, description="Maximum request timeout in seconds")
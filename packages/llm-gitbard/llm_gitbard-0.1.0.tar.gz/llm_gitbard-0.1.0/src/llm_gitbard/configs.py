import llm
from pydantic import BaseModel, Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    PyprojectTomlConfigSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)


class LlmModelSettings(BaseModel):
    name: str | None = Field(default=None, description="Model name")
    api_key: str | None = Field(default=None, description="Model API Key")
    options: dict = Field(default={}, description="Model options")


class CliCommonSettings(BaseSettings):
    model: LlmModelSettings = LlmModelSettings()

    model_config = SettingsConfigDict(
        env_prefix="gitbard_",
        pyproject_toml_table_header=("tool", "gitbard"),
        toml_file=[".gitbard.toml", "gitbard.toml", llm.user_dir() / "gitbard.toml"],
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            PyprojectTomlConfigSettingsSource(settings_cls),
            TomlConfigSettingsSource(settings_cls),
        )

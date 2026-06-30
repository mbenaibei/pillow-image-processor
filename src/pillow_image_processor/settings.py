from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]  # project root dir
ENV_FILE_PATH = BASE_DIR / ".env"


class Settings(BaseSettings):
    images_input_dir: Path
    images_output_dir: Path
    images_output_size: tuple[int, int]
    images_accepted_formats: list[str]
    images_apply_thumbnail: bool
    images_apply_filter_detail: bool
    images_apply_convert_l: bool
    images_apply_quality: int
    images_apply_optimize: bool

    model_config = SettingsConfigDict(
        validate_default=True,
        env_file=ENV_FILE_PATH,
        env_prefix="PIP_",
        env_file_encoding="utf-8",
    )


settings = Settings()

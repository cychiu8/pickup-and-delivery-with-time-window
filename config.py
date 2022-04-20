from pydantic import BaseSettings


class ProjectConfigsSettings(BaseSettings):
    """Config for project."""
    project_path: str = "./"
    log_file_path: str = "data/logs/ai_staffing"
    agg_data_path: str = "data/agg_data/"
    api_key: str = ""


project_config = ProjectConfigsSettings()

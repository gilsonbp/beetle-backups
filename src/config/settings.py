from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = ""
    PROJECT_DESCRIPTION: str = ""
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_DEFAULT_REGION: str = ""
    AWS_ENDPOINT_URL: str = "https://nyc3.digitaloceanspaces.com"
    AWS_SERVICE_NAME: str = "s3"

    AWS_BUCKET_NAME: str = ""
    AWS_ACL: str = "private"

    BACKUP_DIR: str = ""
    BACKUP_DESTINATION_DIR: str = "backups"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

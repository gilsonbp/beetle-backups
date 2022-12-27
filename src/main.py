import os
import re
import logging

from slugify import slugify

from src.config import settings
from src.services.s3_service import S3Service

logger = logging.getLogger(__name__)


def main():
    files = os.listdir(settings.BACKUP_DIR)
    logger.info(f"Start backup from {len(files)} files")

    for file in files:
        file_path = f"{settings.BACKUP_DIR}/{file}"
        pattern = re.compile(r"[^-a-zA-Z0-9.]+")
        filename = slugify(file, regex_pattern=pattern)
        file_dest_path = f"{settings.BACKUP_DESTINATION_DIR}/{filename}"

        logger.info(f"Sending file: [{file}]")
        s3 = S3Service()
        s3.upload(file_path, file_dest_path)

        logger.info(f"Removing file: [{file_path}]")
        os.remove(file_path)

    logger.info(f"End backup from {len(files)} files")


if __name__ == "__main__":
    main()

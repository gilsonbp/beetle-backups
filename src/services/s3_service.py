from boto3 import session

from src.config import settings


class S3Service:
    def __init__(self) -> None:
        self.client = self._client()

    def _client(self):
        s = session.Session()
        return s.client(
            settings.AWS_SERVICE_NAME,
            region_name=settings.AWS_DEFAULT_REGION,
            endpoint_url=settings.AWS_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

    def upload(self, source_file, destination_file):
        self.client.upload_file(
            source_file,
            settings.AWS_BUCKET_NAME,
            destination_file,
            ExtraArgs={"ACL": settings.AWS_ACL},
        )

from uuid import uuid4

import boto3
from botocore.config import Config

from app.core.config import settings

s3_client = boto3.client(
    "s3",
    endpoint_url=settings.b2_endpoint_url,
    aws_access_key_id=settings.b2_key_id,
    aws_secret_access_key=settings.b2_application_key,
    config=Config(signature_version="s3v4"),
    region_name="us-west-004"
)


def build_key(folder: str, filename: str) -> str:
    """Build a unique object key within a given folder prefix."""
    return f"{folder}/{uuid4()}_{filename}"


def get_upload_url(key: str, expires_in: int = 600) -> str:
    """Generate a presigned URL for uploading a file."""
    return s3_client.generate_presigned_url(
        "put_object",
        Params={"Bucket": settings.b2_bucket_name, "Key": key},
        ExpiresIn=expires_in,
    )


def get_read_url(key: str, expires_in: int = 7200) -> str:
    """Generate a presigned URL for reading/viewing a file."""
    return s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.b2_bucket_name, "Key": key},
        ExpiresIn=expires_in,
    )


def upload_file(local_path: str, key: str, content_type: str | None = None):
    """Upload a local file to Backblaze B2."""
    extra_args = {"ContentType": content_type} if content_type else {}
    
    s3_client.upload_file(
        Filename=local_path,
        Bucket=settings.b2_bucket_name,
        Key=key,
        ExtraArgs=extra_args,
    )
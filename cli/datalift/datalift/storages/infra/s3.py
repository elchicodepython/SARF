import boto3
from botocore.exceptions import ClientError

from ..base import (
    StorageDownloader,
    StorageOutput,
    StorageUploader,
)


class S3Storage(StorageUploader, StorageDownloader):
    def __init__(
        self,
        access_key: str,
        secret_key: str,
        endpoint_url: str,
        bucket_name: str,
    ):
        self.__client = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            endpoint_url=endpoint_url,
        )
        self.__bucket_name = bucket_name

    def upload(self, object_name: str, data: bytes) -> StorageOutput:
        """Upload file to S3"""
        try:
            # Check if bucket exists, create it if it does not
            if not self.__bucket_exists(self.__bucket_name):
                self.__create_bucket(self.__bucket_name)

            self.__client.put_object(
                Bucket=self.__bucket_name,
                Key=object_name,
                Body=data
            )
            return StorageOutput("s3", f"{self.__bucket_name}/{object_name}")
        except ClientError as e:
            raise Exception(f"Error uploading object to S3: {e}")

    def download(self, object_name: str) -> bytes:
        """Download file from S3"""
        try:
            response = self.__client.get_object(
                Bucket=self.__bucket_name,
                Key=object_name
            )
            return response['Body'].read()
        except ClientError as e:
            raise Exception(f"Error downloading object from S3: {e}")

    def __bucket_exists(self, bucket_name: str) -> bool:
        """Check if bucket exists"""
        try:
            self.__client.head_bucket(Bucket=bucket_name)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            else:
                raise Exception(f"Error checking bucket existence: {e}")


    def __create_bucket(self, bucket_name: str):
        """Create bucket"""
        try:
            self.__client.create_bucket(Bucket=bucket_name)
        except ClientError as e:
            raise Exception(f"Error creating bucket: {e}")
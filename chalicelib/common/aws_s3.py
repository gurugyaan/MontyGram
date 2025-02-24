import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import tempfile
from datetime import timedelta


class AWSS3:
    def __init__(self, bucket_name, region_name='us-east-1', use_localstack=False):
        self.bucket_name = bucket_name
        self.region_name = region_name
        self.use_localstack = True if os.getenv("ENV") == "local" else False
        self.session = self._create_session()
        self.s3_client = self.session.client('s3', endpoint_url=self._get_endpoint_url())

    def _create_session(self):
        if self.use_localstack:
            # Use dummy credentials for LocalStack
            return boto3.Session(
                aws_access_key_id='test',
                aws_secret_access_key='test',
                region_name=self.region_name
            )
        else:
            # Use environment variables or AWS configuration for actual S3
            return boto3.Session()

    def _get_endpoint_url(self):
        if self.use_localstack:
            return 'http://localhost:4566'
        else:
            return None

    def upload_file(self, file_path, object_name=None):
        """Upload a file to an S3 bucket from a temporary directory."""
        if not object_name:
            object_name = os.path.basename(file_path)

        try:
            self.s3_client.upload_file(file_path, self.bucket_name, object_name)
            print(f"File {file_path} uploaded to {self.bucket_name}/{object_name}")
            return True
        except FileNotFoundError:
            print(f"The file {file_path} was not found")
            return False
        except NoCredentialsError:
            print("Credentials not available")
            return False
        except ClientError as e:
            print(f"Client error: {e}")
            return False

    def download_file(self, object_name, download_path=None):
        """Download a file from an S3 bucket to a temporary directory."""
        if not download_path:
            download_path = os.path.join(tempfile.gettempdir(), object_name)

        try:
            self.s3_client.download_file(self.bucket_name, object_name, download_path)
            print(f"File {object_name} downloaded to {download_path}")
            return download_path
        except NoCredentialsError:
            print("Credentials not available")
            return None
        except ClientError as e:
            print(f"Client error: {e}")
            return None

    def create_signed_url(self, object_name, expiration=3600):
        """Generate a presigned URL to share an S3 object."""
        try:
            response = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': object_name},
                ExpiresIn=expiration
            )
            print(f"Signed URL for {object_name}: {response}")
            return response
        except ClientError as e:
            print(f"Client error: {e}")
            return None

    def delete_s3_object(self, object_key):
        try:
            response = self.s3_client.delete_object(Bucket=self.bucket_name, Key=object_key)
            print(f"Deleted {object_key} from {self.bucket_name}.")
            return response
        except ClientError as e:
            print(f"Error deleting object: {e}")
            return None
import os
import boto3
import tempfile


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
        if not object_name:
            object_name = os.path.basename(file_path)

        try:
            self.s3_client.upload_file(file_path, self.bucket_name, object_name)
            print(f"File {file_path} uploaded to {self.bucket_name}/{object_name}")
            return True
        except Exception as err:
            print(err)

    def download_file(self, object_name, download_path=None):
        if not download_path:
            download_path = os.path.join(tempfile.gettempdir(), object_name)

        try:
            self.s3_client.download_file(self.bucket_name, object_name, download_path)
            print(f"File {object_name} downloaded to {download_path}")
            return download_path
        except Exception as err:
            print(err)

    def create_signed_url(self, object_name, expiration=3600):
        try:
            response = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': object_name},
                ExpiresIn=expiration
            )
            print(f"Signed URL for {object_name}: {response}")
            return response
        except Exception as err:
            print(err)

    def delete_s3_object(self, object_key):
        try:
            response = self.s3_client.delete_object(Bucket=self.bucket_name, Key=object_key)
            print(f"Deleted {object_key} from {self.bucket_name}.")
            return response
        except Exception as err:
            print(f"Error deleting object: {err}")
            return None
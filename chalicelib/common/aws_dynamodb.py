import os
import boto3
from boto3.dynamodb.conditions import Key

class AWSDynamoDB:
    def __init__(self, table_name):
        self.table_name = table_name
        self.region_name = os.getenv("AWS_REGION")
        self.use_localstack = True if os.getenv("ENV") == "local" else False
        print(os.getenv("ENV"))
        if self.use_localstack:
            # Use LocalStack endpoint
            self.dynamodb = self._setup_localstack()
        else:
            # Use AWS DynamoDB
            self.dynamodb = boto3.resource('dynamodb', region_name=self.region_name)
        self.table = self.dynamodb.Table(table_name)

    def _setup_localstack(self):
        local_dynamodb = boto3.resource(
                'dynamodb',
                endpoint_url='http://localhost:4566',
                region_name='us-east-1',
                aws_access_key_id='test',
                aws_secret_access_key='test'
            )
        print("Connecting to localstack")
        return local_dynamodb


    def insert_record(self, item):
        try:
            self.table.put_item(Item=item)
            return {'message': 'Record inserted successfully'}
        except Exception as err:
            return {'error': str(err)}

    def fetch_records_by_pk(self, pk_value, pk='partition_key'):
        try:
            response = self.table.query(
                KeyConditionExpression=Key(pk).eq(pk_value)
            )
            return response.get('Items', [])
        except Exception as err:
            return {'error': str(err)}

    def fetch_record_by_pk_sk(self, pk_value, sk_value, pk='partition_key', sk='sort_key'):
        try:
            response = self.table.query(
                KeyConditionExpression=(
                    Key(pk).eq(pk_value) &
                    Key(sk).eq(sk_value)
                )
            )
            return response.get('Items', [])
        except Exception as err:
            return {'error': str(err)}

    def scan_all(self):
        try:
            response = self.table.scan()
            return response.get('Items', [])
        except Exception as err:
            return {'error': str(err)}

    def delete_record(self, pk_value, sk_value=None, pk='partition_key', sk='sort_key'):
        key = {pk: pk_value}
        if sk_value:
            key[sk] = sk_value
        try:
            self.table.delete_item(Key=key)
            return {'message': 'Record deleted successfully'}
        except Exception as err:
            return {'error': str(err)}
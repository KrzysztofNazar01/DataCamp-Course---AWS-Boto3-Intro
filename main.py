import os
from dotenv import load_dotenv
import boto3
import json
from datetime import datetime
from dateutil import tz


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            # Convert datetime objects to ISO 8601 format strings
            return obj.isoformat()
        return super().default(obj)


def print_formatted_json(data):
    # Convert the dictionary to a pretty JSON string
    formatted_json = json.dumps(data, indent=4, cls=DateTimeEncoder)
    print(formatted_json)


def get_s3_buckets(client):
    resposne = client.list_buckets()

    print_formatted_json(resposne['Buckets'])


def get_sns_topics(client_s3, client_sns):
    # List S3 buckets and SNS topics
    buckets = client_s3.list_buckets()
    topics = client_sns.list_topics()

    # Print out the list of SNS topics
    print_formatted_json(topics)


def create_bucket(client_s3):
    # Create the buckets
    response_staging = client_s3.create_bucket(Bucket='bucketforsg')

    # Print out the response
    print_formatted_json(response_staging)


def iterate_over_buckets(client_s3):
    # Get the list_buckets response
    response = client_s3.list_buckets()

    # Iterate over Buckets from .list_buckets() response
    for bucket in response['Buckets']:
        # Print the Name for each bucket
        print(bucket['Name'])


def delete_bucket(client_s3):
    # Delete the gim-test bucket
    client_s3.delete_bucket(Bucket='elasticbeanstalk-eu-central-1-663217569446')

    # Get the list_buckets response
    response = client_s3.list_buckets()

    # Print each Buckets Name
    for bucket in response['Buckets']:
        print(bucket['Name'])


def upload_a_file_and_get_metadata(client_s3):
    # TODO: test
    # Upload final_report.csv to gid-staging
    client_s3.upload_file(Bucket='gid-staging',
                   # Set filename and key
                   Key='2019/final_report_01_01.csv',
                   Filename='final_report.csv')

    # Get object metadata and print it
    response = s3.head_object(Bucket='gid-staging',
                              Key='2019/final_report_01_01.csv')

    # Print the size of the uploaded object
    print(response['ContentLength'])


def delete_objects_from_bucket(client_s3):
    # TODO: test
    # List only objects that start with '2018/final_'
    response = client_s3.list_objects(Bucket='gid-staging',
                               Prefix='2018/final_')

    # Iterate over the objects
    if 'Contents' in response:
        for obj in response['Contents']:
            # Delete the object
            client_s3.delete_object(Bucket='gid-staging', Key=obj['Key'])

    # Print the keys of remaining objects in the bucket
    response = client_s3.list_objects(Bucket='gid-staging')

    for obj in response['Contents']:
        print(obj['Key'])



if __name__ == '__main__':
    load_dotenv()
    AWS_KEY_ID = os.getenv('AWS_KEY_ID')
    AWS_SECRET = os.getenv('AWS_SECRET')

    client_s3 = boto3.client('s3',
                             region_name='eu-central-1',
                             aws_access_key_id=AWS_KEY_ID,
                             aws_secret_access_key=AWS_SECRET)

    client_sns = boto3.client('sns',
                              region_name='eu-central-1',
                              aws_access_key_id=AWS_KEY_ID,
                              aws_secret_access_key=AWS_SECRET)

    get_s3_buckets(client_s3)
    # get_sns_topics(client_s3, client_sns)
    delete_bucket(client_s3)

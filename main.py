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


def get_s3_buckets(AWS_KEY_ID, AWS_SECRET, aws_region):
    load_dotenv()
    s3 = boto3.client('s3',
                      region_name=aws_region,
                      aws_access_key_id=AWS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET)
    resposne = s3.list_buckets()

    print_formatted_json(resposne)


def get_sns_topics(AWS_KEY_ID, AWS_SECRET, aws_region):
    # Generate the boto3 client for interacting with S3 and SNS
    s3 = boto3.client('s3', region_name=aws_region,
                      aws_access_key_id=AWS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET)

    sns = boto3.client('sns', region_name=aws_region,
                       aws_access_key_id=AWS_KEY_ID,
                       aws_secret_access_key=AWS_SECRET)

    # List S3 buckets and SNS topics
    buckets = s3.list_buckets()
    topics = sns.list_topics()

    # Print out the list of SNS topics
    print_formatted_json(topics)


if __name__ == '__main__':
    load_dotenv()
    AWS_KEY_ID = os.getenv('AWS_KEY_ID')
    AWS_SECRET = os.getenv('AWS_SECRET')

    get_s3_buckets(AWS_KEY_ID, AWS_SECRET, 'eu-central-1')
    get_sns_topics(AWS_KEY_ID, AWS_SECRET, 'eu-central-1')

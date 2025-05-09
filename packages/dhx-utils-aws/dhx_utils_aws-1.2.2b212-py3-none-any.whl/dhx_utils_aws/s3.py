"""
Copyright (c) 2021 RoZetta Technology Pty Ltd. All rights reserved.
"""
from typing import Dict, Tuple, Any
from urllib.parse import urlparse

import boto3
import simplejson as json
from dhx_utils.errors import APIError


def parse_s3_bucket_and_key(s3_uri: str) -> Tuple:
    """ To split an S3 URI into 2 parts, the bucket and the key.

    :param s3_uri: The S3 URI to split.
    :return: Tuple of strings (bucket, key)
    """
    parts = urlparse(s3_uri)
    bucket = parts.netloc
    key = parts.path.lstrip('/')
    return bucket, key


def read_s3_json_object(s3_uri: str) -> Dict:
    """ Reads and parse a JSON object located in s3.

    :param s3_uri: The S3 path that contains the JSON object.
    :return: A dictionary object parsed from the JSON object.
    """
    bucket, key = parse_s3_bucket_and_key(s3_uri)
    try:
        s3_client = boto3.client('s3')
        result = s3_client.get_object(Bucket=bucket, Key=key)
        return json.loads(result['Body'].read().decode('utf-8'))
    except Exception as e:
        raise APIError(f"Unable to read the JSON file: {s3_uri}") from e


def write_s3_json_object(s3_uri: str, payload: Dict[str, Any]):
    """ Reads and parse a JSON object, then writes to S3.

    :param s3_uri: The S3 path that contains the JSON object.
    :param payload: dictionary that contains the JSON object to write.
    """
    bucket, key = parse_s3_bucket_and_key(s3_uri)
    try:
        s3_client = boto3.client('s3')
        s3_client.put_object(Body=json.dumps(payload), Bucket=bucket, Key=key)
    except Exception as e:
        raise APIError(f"Unable to save the JSON file to {s3_uri}") from e

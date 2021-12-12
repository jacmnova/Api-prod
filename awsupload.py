import boto3
from botocore.vendored import requests
import base64
import logging
import boto3
from botocore.exceptions import ClientError
from os import remove
import os

# Let's use Amazon S3
# s3 = boto3

#
# Bucket Front Test: test-cobra-console
#              Prod: prod-cobra-web
#
# CloudFront Test: E2MMROZTDGUAI8
#            Prod: E7CU0AY3J2Q1J

aws_access_key_id = 'AKIAW2IQ2V375GLCMQGA'
aws_secret_access_key = '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'
region_name = 'us-east-1'
cdn = 'https://cdn.clinicacobra-app.com.br/'

session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)
s3 = session.resource('s3')


def upload(info):
    print(info)
    image_base64 = info['base64']
    format_img = info['format']
    nameBucket = info['name']
    name = info['name'].split("/")[1]

    fh = open(name, "wb")
    fh.write(base64.b64decode(image_base64))
    fh.close()

    try:
        data = open(name, 'rb')
        s3.Bucket('cobra-cdn').put_object(Key='photos/' + nameBucket, Body=data)
        data.close()
    except ClientError as e:
        logging.error(e)

    remove(name)

    return cdn + 'photos/' + nameBucket


# for bucket in s3.buckets.all():
#     print(bucket.name)# Print out auto scaling groups names
#     # {
#     #
#     #     'format': 'png', 'name': 'f98778de4c2fbdeef15b745b380077ce745555bd/adic_0.png'}
#

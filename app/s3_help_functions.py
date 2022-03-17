import os

import boto3
import json
from botocore.errorfactory import ClientError
from smart_open import smart_open

from constans import BUCKET_NAME

s3 = boto3.client("s3")

# To create folder
def create_folder_s3(folder_name):
    return s3.put_object(Bucket=BUCKET_NAME, Key=folder_name)

# To read coolies
def read_json_cookies_s3(username):
    s3_clientobj = s3.get_object(Bucket=BUCKET_NAME, Key=f'profile/{username}/cookies/{username}_cookies.json')
    s3_clientdata = json.load(s3_clientobj['Body'])
    return s3_clientdata

# To read user info
def read_json_user_info_s3(username):
    s3_clientobj = s3.get_object(Bucket=BUCKET_NAME, Key=f'profile/{username}/{username}.json')
    s3_clientdata = json.load(s3_clientobj['Body'])
    return s3_clientdata


def file_exist_s3(filename_in_s3):
    try:
        s3.get_object(Bucket=BUCKET_NAME, Key=filename_in_s3)
        return True
    except ClientError:
        return False

def read_user_info_s3(username):
    s3_clientobj = s3.get_object(Bucket=BUCKET_NAME, Key=f'profile/{username}/{username}.json')
    s3_clientdata = json.load(s3_clientobj['Body'])
    return s3_clientdata

def read_posts_url(username, file_name):
    url_list = list()
    for line in smart_open(f's3://{BUCKET_NAME}/profile/{username}/{file_name}', 'rb'):
        url_list.append(line.decode('utf8').split('\n')[0])
    return url_list


# To upload files
def upload_to_aws(local_file_name, filename_in_s3):
    try:
        s3.upload_file(local_file_name, BUCKET_NAME, filename_in_s3)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False

# To create, load to S3 and delete tmp file
def final_file_cheker(local_file_name, filename_in_s3):
    upload_to_aws(local_file_name, filename_in_s3)
    if file_exist_s3(filename_in_s3):
        os.remove(local_file_name)
    else: print("File not loaded")


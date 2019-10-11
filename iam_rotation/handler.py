#	Author:	@vipink1203
# 	Description: API endpoint will take an IAM Access key as query parameter and will check for the user associated with that key. 
#                If the key is valid it will create a new key pair and display it. 
#                You need to have additional lambda functions for IAM key rotation.
#	Last	Edited:	October 11 2019

import json
import boto3
import datetime
import sys

iam = boto3.client('iam')
details = iam.list_users()
access_details = []
ERROR_RESPONSE = {
    'statusCode': 400,
    'body': json.dumps('Oops, Invalid IAM key')
}

def time_diff(createdtime):
    now=datetime.datetime.now(datetime.timezone.utc)
    diff=now-createdtime
    return diff.days


def iam_check(event, context):
    current_key = event["queryStringParameters"]["currentKey"]
    print(current_key)
    for i in details['Users']:
        keydetails = iam.list_access_keys(UserName=i['UserName'])
        for j in keydetails['AccessKeyMetadata']:     
            access_details.append(j)
    for k in access_details:
        if k['Status'] == 'Active' and current_key == k['AccessKeyId'] and (time_diff(k['CreateDate'])) >= 7:
            resp = iam.create_access_key(
                UserName=k['UserName']
            )
            access_keys = resp['AccessKey']
            final_keys = {}
            final_keys['AccessID'] = access_keys["AccessKeyId"]
            final_keys['SecretAccessKey'] = access_keys["SecretAccessKey"]
            OK_RESPONSE = {
                'statusCode': 200,
                'body' : json.dumps(final_keys)
            }
            return OK_RESPONSE
    else:
        return ERROR_RESPONSE

import json
import boto3

s3=boto3.client("s3")

def lambda_handler(event, context):
    
shaHash = event['pathParameters']['shaHash']

    if len(shaHash) == 40:
        file_content = s3.get_object(
            Bucket=S3_BUCKET, Key="sha1.json")["Body"]
        lookupTable = json.loads(file_content)
        passwordCode = lookupTable.get(shaHash)
    elif len(shaHash) == 64:
        file_content = s3.get_object(
            Bucket=S3_BUCKET, Key="sha256.json")["Body"]
        lookupTable = json.loads(file_content)
        passwordCode = lookupTable.get(shaHash)
    else:
        return{
            'statusCode': 404,
            'body': json.dumps({"Not Hash-1 or Hash-256 code"})
        }

    if passwordCode == None:
        return{
            'statusCode': 404,
            'body': json.dumps({"Hash was not found in lookup table"})
        }
    return {
            'statusCode': 200,
            'body': json.dumps({shaHash:passwordCode})
        }
        
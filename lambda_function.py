import json
import boto3

    
def lambda_handler(event, context):
    
    shaHash = event['pathParameters']['shaHash']
    s3 = boto3.client('s3')
    resp = s3.select_object_content(
        Bucket = 'cs561samueltable',
        Key = 'sha1256.csv',
        ExpressionType = 'SQL',
        Expression = f"Select * from s3object s where s.\"key\"='{shaHash}'",
        InputSerialization = {'CSV': {"FileHeaderInfo": "Use"}, 'CompressionType': 'None'},
        OutputSerialization = {'JSON': {}},
    )

    for event in resp['Payload']:
        if 'Records' in event:
            records = json.loads(event['Records']['Payload'].decode('utf-8'))
            return {
                'statusCode': 200,
                'headers': {
                "Access-Control-Allow-Headers" : "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                },
                'body': json.dumps({records['key']:records['value'].strip()})
            }
        else:
            return{
                'statusCode': 404,
                'headers': {
                "Access-Control-Allow-Headers" : "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                },
                'body': json.dumps(" message : Not in SHA-1 or SHA-256 dictionary ")
            }
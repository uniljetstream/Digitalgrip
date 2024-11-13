import json
import boto3
import logging
 
logger = logging.getLogger()
logger.setLevel(logging.INFO)
 
client = boto3.client('iot-data')
 
def lambda_handler(event, context):
    print(json.dumps(event['body']))
    
    body = event['body']
    body = json.loads(body)
    
    THINGNAME=body['thingname']
    if (THINGNAME == ""):
        print("No Thing Name found. Setting Thing Name = test1")
        THINGNAME="test1"
    
    if body['action'] == "on":
        payload = json.dumps({'state': { 'desired': { 'status': 'on' } }})
        
        logger.info("Attempting to Update Shadow State to ON")
        response = client.update_thing_shadow(
            thingName=THINGNAME,
            payload=payload
        )
        logger.info("IOT Shadow Updated")
    else:
        payload = json.dumps({'state': { 'desired': { 'status': 'off' } }})
        
        logger.info("Attempting to Update Shadow State to OFF")
        response = client.update_thing_shadow(
            thingName=THINGNAME,
            payload=payload
        )
        logger.info("IOT Shadow Updated")
        
    
    return {
        'statusCode': 200,
        "headers": {
            'Access-Control-Allow-Origin':'*',
            'Access-Control-Allow-Headers':'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods':'GET,OPTIONS'
        },
        'body': json.dumps('Shadow Updated!')
    }
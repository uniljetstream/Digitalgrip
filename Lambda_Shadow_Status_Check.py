import json
import boto3
import logging
 
logger = logging.getLogger()
logger.setLevel(logging.INFO)
 
client = boto3.client('iot-data')
 
def lambda_handler(event, context):
    
    # print(json.dumps(event))
    print("Thing Name: " + json.dumps(event['queryStringParameters']['thingname']))
    
    logger.info("Attempting to fetch Shadow State")
    
    THINGNAME=event['queryStringParameters']['thingname']
    if (THINGNAME == ""):
        print("No Thing Name found. Setting Thing Name = test1")
        THINGNAME="test1"
    
    try:
        response = client.get_thing_shadow(thingName=THINGNAME)
        logger.info("Shadow State Received")
        res = response['payload'].read()
        res_json = json.loads(res)
        print(json.dumps(res_json))
        
        status = res_json['state']['reported']
        
        logger.info("Received From IoT: " + json.dumps(status))
        
        logger.info("\nChanging for website\n")
     
        value = status['status']
        if (value == "on"):
            status['status'] = "It's On"
        else:
            status['status'] = "It's Off"
        
        logger.info("Sending to Website: " + json.dumps(status) + "\n")
        
        return {
            'statusCode': 200,
            "headers": {
                'Access-Control-Allow-Origin':'*',
                'Access-Control-Allow-Headers':'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods':'GET,OPTIONS'
            },
            'body': json.dumps(status)
        }
    except:
        status = {"status": "Device Shadow State Error"}
        return {
            'statusCode': 200,
            "headers": {
                'Access-Control-Allow-Origin':'*',
                'Access-Control-Allow-Headers':'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods':'GET,OPTIONS'
            },
            'body': json.dumps(status)
        }


import boto3
import botocore
import simplejson as json
import time
import jwt
from constants import *




def getDbUserNameAndPassword():
    secret_name = "rds-portal-credentials-name"
    region_name = "eu-central-1"
    session = boto3.Session()
    client = session.client(
        service_name="secretsmanager",
        region_name=region_name
    )
    secretResponse = None
    credentials = None
    try:
        secretResponse = client.get_secret_value(
            SecretId=secret_name
        )
    except botocore.exceptions.ClientError as e:
        print("ERROR {}".format(e))
    if "SecretString" in secretResponse:
        credentials = secretResponse["SecretString"]
    credentialsObject = json.loads(credentials)
    returnObject = {
        "username": credentialsObject["username"],
        "host": credentialsObject["host"],
        "dbname": credentialsObject["dbname"],
        "password": credentialsObject["password"]                               
    }
    return returnObject

def getSecretKey():
    try:
        secretKeyArn = "arn:aws:secretsmanager:eu-central-1:823342781857:secret:uatokenapisecrettokensecret-a3LuOqPnG6pK-0iBDai"
        secretResponse = boto3.client("secretsmanager").get_secret_value(SecretId="uatokenapisecrettokensecret-gHbe07HUUg4Q")
        secretJson = json.loads(secretResponse['SecretString'])
        secret_key = secretJson['secretKey']
    except:
        secret_key = None
    return secret_key

def validateToken(token):
    secretKey = getSecretKey()
    print("secretkey is {}".format(secretKey))
    jwtPayload = jwt.decode(token, secretKey, algorithms=[ALGORITHM])
    return jwtPayload
      
def validateRequest(event):
    validateJson = None
    token = None
    print("The validation event queryStrings is {}".format(event["queryStringParameters"]))
    if "queryStringParameters" in event:
        if "token" in event["queryStringParameters"]:
            token = event["queryStringParameters"]["token"]
    if ("Authorization" in event["headers"]) and (token == None):
        print("The header is {}".format(event["headers"]["Authorization"]))
        token = event["headers"]["Authorization"]
    if token != None:
        payload = validateToken(token)
        print("payload is {}".format(payload))
        expiration = payload["exp"]
        actTime = time.time()
        print("The exp is {}, the actTime is {}".format(int(expiration), int(actTime)))
        if (int(expiration) >= int(actTime)):
            if "AccountId" in payload: 
                return {"accountId" : payload["AccountId"],
                        "Id" : payload["Id"],
                        "exp" : payload["exp"],
                        }
            else:
                return payload
    else:
        validateJson = None
    return validateJson
    
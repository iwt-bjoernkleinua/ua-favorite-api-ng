import boto3
import botocore
import simplejson as json




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
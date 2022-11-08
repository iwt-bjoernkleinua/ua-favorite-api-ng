from httpResponse import *
from helper import *
import simplejson as json
import pymysql
from helper import getDbUserNameAndPassword


def deleteFavorite(event):
    
    try:
        accountId = event["queryStringParameters"]["accountId"]
        relocationId = event["queryStringParameters"]["relocationId"]

        credentials = getDbUserNameAndPassword()
        db = pymysql.connect(host=credentials["host"], user=credentials["username"], passwd=credentials["password"], database=credentials["dbname"])
        cursor = db.cursor()      
        sql = "DELETE FROM `Favorites`  WHERE `accountId` = %s and  `relocationId` = %s"
        print("I am here")
        result = cursor.execute(sql, (accountId, relocationId))
        db.commit()
        print("Result is {}".format(result))
           
        response = HttpResponse.buildJsonResponse(
            status_code=200,
            body="deleted Favorite for {} on {}".format(accountId, relocationId)
        )
    except:
        response = HttpResponse.buildResponse(
            status_code=501,
            body="Please provide valid accountId and relocationId"
        )
        
    return response

from httpResponse import *
from helper import *
import simplejson as json
import pymysql
from helper import getDbUserNameAndPassword



def addFavorite(event):

    try:
        accountId = event["queryStringParameters"]["accountId"]
        relocationId = event["queryStringParameters"]["relocationId"]

        credentials = getDbUserNameAndPassword()
        db = pymysql.connect(host=credentials["host"], user=credentials["username"], passwd=credentials["password"], database=credentials["dbname"])
        cursor = db.cursor()      
        sql = "SELECT `accountId`, `relocationId` from `Favorites` WHERE `accountId` = %s and  `relocationId` = %s"
        result = cursor.execute(sql, (accountId, relocationId))

        if result == 0:
            sql = "INSERT INTO `Favorites` (`accountId`, `relocationId`) VALUES (%s, %s)"
            result = cursor.execute(sql,(accountId, relocationId))
            db.commit()
            
        response = HttpResponse.buildJsonResponse(
            status_code=200,
            body="added favorite for {} on {}".format(accountId, relocationId)
        )
    except:
        response = HttpResponse.buildResponse(
            status_code=501,
            body="Please provide valid accountId and relocationId"
        )
        
    return response
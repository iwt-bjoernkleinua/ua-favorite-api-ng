import decimal
from httpResponse import HttpResponse
import boto3
import os
from constants import *
import simplejson
import base64
import botocore.exceptions
import simplejson as json
from favoriteAdd import addFavorite
from favoriteDelete import deleteFavorite





def UaFavoriteApiNgEndpointHandler(event, context):
    if event["httpMethod"] == "POST":
        if event["path"] == "/add":
            return addFavorite(event)

        if event["path"] == "/delete":
            return deleteFavorite(event)
            
            
    elif event["httpMethod"] == "POST":
        if event["path"] == "/":
            return None
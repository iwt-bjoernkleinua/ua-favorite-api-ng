import constants


class HttpResponse:

    @staticmethod
    def buildResponse(*, status_code=200, content_type=constants.TEXT_PLAIN, body=""):
        return {
            "statusCode": status_code,
            "headers": {
                "Content-Type": content_type,
                "Access-Control-Allow-Origin": constants.ALLOW_ORIGIN,
                "Access-Control-Allow-Methods": constants.ALLOW_METHODS,
                "Access-Control-Allow-Headers": constants.ALLOW_HEADERS
            },
            "body": body
        }

    @staticmethod
    def buildJsonResponse(*, status_code=200, content_type=constants.APPLICATION_JSON, body=""):
        return HttpResponse.buildResponse(status_code=status_code, content_type=content_type, body=body)
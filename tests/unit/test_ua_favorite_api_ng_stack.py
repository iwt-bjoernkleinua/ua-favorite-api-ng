import aws_cdk as core
import aws_cdk.assertions as assertions

from ua_favorite_api_ng.ua_favorite_api_ng_stack import UaFavoriteApiNgStack

# example tests. To run these tests, uncomment this file along with the example
# resource in ua_favorite_api_ng/ua_favorite_api_ng_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = UaFavoriteApiNgStack(app, "ua-favorite-api-ng")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })

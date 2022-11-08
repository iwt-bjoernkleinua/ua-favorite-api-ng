#!/usr/bin/env python3
import os

import aws_cdk as cdk

from ua_favorite_api_ng.ua_favorite_api_ng_stack import UaFavoriteApiNgStack


app = cdk.App()
stage = app.node.try_get_context("stage")
UaFavoriteApiNgStack(app, "UaFavoriteApiNgStack",
                     env=cdk.Environment(account=os.getenv("AWS_ACCOUNT"),
                                           region=os.getenv("AWS_REGION")
                       ),
                        stage=stage
    )

app.synth()

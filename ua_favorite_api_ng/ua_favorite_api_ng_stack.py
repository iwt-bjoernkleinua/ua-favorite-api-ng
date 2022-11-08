from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as _lambda,
    aws_lambda_python_alpha as _alambda,
    aws_apigateway as _apiGw,
    aws_certificatemanager as _cm,
    aws_route53 as _r53,
    aws_route53_targets as _r53Tartgets,
    aws_iam as _iam,
    aws_ec2 as _ec2
)
from constructs import Construct
from ua_favorite_api_ng import rootDomain, memorySize

class UaFavoriteApiNgStack(Stack):
    
    def buildApiGateway(self):
        route53HostedZone = _r53.HostedZone.from_lookup(
            self, "{}Zone".format(self.stackPrefix),
            domain_name=self.rootDomain
        )
        
        lambdaExecutionRole = _iam.Role(self,
                                        id="uaFavoriteApiNgLambdaExecutionRole",
                                        role_name="uaFavoriteApiNgLambdaExecutionRole",
                                        assumed_by=_iam.ServicePrincipal("lambda.amazonaws.com"),
                                        managed_policies=[
                                            _iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
                                            _iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaVPCAccessExecutionRole"),
                                            _iam.ManagedPolicy.from_aws_managed_policy_name("AmazonVPCFullAccess"),
                                            _iam.ManagedPolicy.from_aws_managed_policy_name("SecretsManagerReadWrite")   
                                            ]
                                        )
        
        cmCert = _cm.Certificate(
            self, "ua-favorite-api-ng-cert",
            domain_name=self.dnsRecordName,
            validation=_cm.CertificateValidation.from_dns(route53HostedZone)
        )
        
        uaPortalVpc = _ec2.Vpc.from_lookup(self,id="vpc-0c284d247dcc4e7ec", vpc_name="UaPortalDbStack/portal-db-vpc")
        
        privateSubnets = _ec2.SubnetSelection(
                subnets=uaPortalVpc.select_subnets(subnet_group_name="PrivateRDSSubnet").subnets
            )       
        
        favoriteHandler = _alambda.PythonFunction(
            self,
            "ua-favorite-handler-ng",
            runtime=_lambda.Runtime.PYTHON_3_9,
            entry="./lambda/",
            index="uaFavoriteApiEndpoint.py",
            handler="UaFavoriteApiNgEndpointHandler",
            timeout=Duration.seconds(30),
            memory_size=self.memorySize,
            role=lambdaExecutionRole,
            vpc=uaPortalVpc,
            vpc_subnets=privateSubnets,
            security_groups=[_ec2.SecurityGroup.from_lookup_by_id(scope=self,id="mySecGroup",security_group_id="sg-00c5906dbb9bf3884")]
        )
        
        corsPreflight = _apiGw.CorsOptions(
            allow_headers=_apiGw.Cors.ALL_ORIGINS,
            allow_origins=_apiGw.Cors.ALL_ORIGINS,
            allow_methods=_apiGw.Cors.ALL_METHODS,
            status_code=200
        )
        
        favoriteApi = _apiGw.LambdaRestApi(
            self,
            self.stackPrefix,
            handler=favoriteHandler,
            domain_name=_apiGw.DomainNameOptions(
                domain_name=self.dnsRecordName,
                certificate=cmCert
            ),
            endpoint_types=[_apiGw.EndpointType.REGIONAL],
            deploy_options=self.stageDeployment,
            default_cors_preflight_options=corsPreflight,
            proxy=False
        )
        
        favoriteProxy = favoriteApi.root.add_proxy(
            any_method=False,
            default_cors_preflight_options=corsPreflight,
            default_method_options=_apiGw.MethodOptions(
                api_key_required=False
            )
        )
        
        favoriteProxy.add_method(http_method="ANY",
                                   api_key_required=True)
        
        apiKey = favoriteApi.add_api_key(
            "uaFavoriteNgApiKey",
            api_key_name=self.apiKeyName,
            value=self.apiKeyValue
        )
        
        throttleSetting = _apiGw.ThrottleSettings(
            burst_limit=300,
            rate_limit=200
        )
        
        usagePlan = favoriteApi.add_usage_plan("favoriteApiNgUsagePlan",
                                                throttle=throttleSetting
                                                )
        
        usagePlan.add_api_stage(stage=favoriteApi.deployment_stage)
        usagePlan.add_api_key(api_key=apiKey)
        
        _r53.ARecord(
            self,
            "AliasRecord",
            record_name=self.record_name,
            zone=route53HostedZone,
            target=_r53.RecordTarget.from_alias(_r53Tartgets.ApiGateway(favoriteApi))
        )

    def __init__(self, scope: Construct, construct_id: str, stage: str = "dev", **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.stackPrefix = "ua-favorite-api-ng"
        self.stage = stage
        self.apiKeyName = "{}-{}".format(self.stackPrefix, self.stage)
        self.apiKeyValue = "qh5avq9x9kw89nwpwwssc8atwi8eKlhG658Gh5FB"
        self.stageDeployment = _apiGw.StageOptions(
            stage_name=self.stage,
            variables={
                "stage": self.stage
            }
        )
        self.memorySize = memorySize[stage]
        self.rootDomain = rootDomain[stage]
        self.record_name = self.stackPrefix
        self.dnsRecordName = "{}.{}".format(self.stackPrefix, rootDomain[stage])
        self.buildApiGateway()
 
from aws_cdk import (
    CfnOutput,
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_route53 as route53,
    aws_certificatemanager as acm,
    aws_route53_targets as targets,
)

from cdk_aws_lambda_powertools_layer import LambdaPowertoolsLayer

from constructs import Construct


class TaskerApiStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, domain_name: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a Hosted Zone
        hosted_zone = route53.HostedZone.from_lookup(
            self, "HostedZone", domain_name=domain_name)
        
        # Creat a Certificate
        # This means that ACM will create DNS records in the specified
        # hosted zone to prove ownership of the domain
        certificate = acm.Certificate(
            self, "Certificate",
            domain_name=domain_name,
            validation=acm.CertificateValidation.from_dns(hosted_zone))

        # Define the AWS LambdaPowertools Layer once so we can reuse it
        power_tools_layer = LambdaPowertoolsLayer(self, "LambdaPowertoolsLayer")

        # Define the Lambda function with the API Gateway Resolver
        Lambda_function = _lambda.Function(
            self, "TaskerApiLambda",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="api_resolver.handler",
            code=_lambda.Code.from_asset("lambda"),
            layers=[power_tools_layer],
            environment={
                "DOMAIN_NAME": domain_name,
                "POWERTOOLS_SERVICE_NAME": "TASKER_API",
                "POWER_TOOLS_LOG_LEVEL": "INFO",
            },
        )

        # Create an API Gateway
        api = apigateway.LambdaRestApi(
            self, "TaskerApi",
            rest_api_name="TaskerApi",
            description="This API handles Tasking operations",
            handler=Lambda_function,
            proxy=False
        )

        tasks = api.root.add_resource("tasks")
        tasks.add_method("GET") # GET /tasks
        tasks.add_method("POST") # POST /tasks

        id = tasks.add_resource("{id}")
        id.add_method("GET") # GET /task/{id}
        id.add_method("PUT") # PUT /task/{id}
        id.add_method("DELETE") # DELETE /task/{id}

        api_domain = apigateway.DomainName(
            self, "TaskerApiDomain",
            domain_name=domain_name,
            certificate=certificate,
            endpoint_type=apigateway.EndpointType.REGIONAL
        )

        # Add base path mapping to the API
        apigateway.BasePathMapping(self, "ApiMapping",
            domain_name=api_domain,
            rest_api=api
        )

        # Add ARecord to the Hosted Zone
        route53.ARecord(
            self, "ApiAliasRecord",
            zone=hosted_zone,
            target=route53.RecordTarget.from_alias(
                targets.ApiGatewayDomain(api_domain)
            )
        )

        # Output the API Gateway URL
        CfnOutput(self, "APIGatewayURL",
                  value=f"https://{api_domain.domain_name}")

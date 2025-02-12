#!/usr/bin/env python3
import os

import aws_cdk as cdk

from crud_api_lambda.crud_api_lambda_stack import CrudApiLambdaStack

account = os.getenv('AWS_ACCOUNT_ID')
primary_region = os.getenv('AWS_PRIMARY_REGION')
domain_name = os.getenv('AWS_DOMAIN_NAME')

primary_environment = cdk.Environment(account=account, region=primary_region)

app = cdk.App()
CrudApiLambdaStack(app, "CrudApiLambdaStack",
                    domain_name=domain_name,
                    env=primary_environment)

app.synth()

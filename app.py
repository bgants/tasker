#!/usr/bin/env python3
import os
import aws_cdk as cdk
from tasker_api.tasker_api import TaskerApiStack

# Make sure you have dcoker installed and running, this is used to build the lambda layer.
# If you see Error: spawnSync docker ENOENT when running cdk synth, it means docker is not installed or not running.


# Set up environment variables
account = os.getenv('AWS_ACCOUNT_ID')
primary_region = os.getenv('AWS_PRIMARY_REGION')
domain_name = os.getenv('AWS_DOMAIN_NAME', 'default-domain-name')

primary_environment = cdk.Environment(account=account, region=primary_region)

app = cdk.App()
TaskerApiStack(app, 'TaskerApiStack',
                    domain_name=domain_name,
                    env=primary_environment)

app.synth()

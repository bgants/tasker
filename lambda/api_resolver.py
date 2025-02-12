from aws_lambda_powertools import Logger
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext
from aws_lambda_powertools.event_handler import APIGatewayRestResolver

logger = Logger()
app = APIGatewayRestResolver()

@app.get("/transactions")
def get_transactions():
    return {
        "statusCode": 200,
        "body": "Hello from Lambda!"
    }

@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
def handler(event: dict, context: LambdaContext) -> dict:
    logger.info(f" Event: {event}")
    return app.resolve(event, context)
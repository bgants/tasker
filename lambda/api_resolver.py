from aws_lambda_powertools import Logger
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext
from aws_lambda_powertools.event_handler import APIGatewayRestResolver

logger = Logger()
app = APIGatewayRestResolver()

@app.get("/items")
def get_items():
    return {
        "statusCode": 200,
        "body": "Get all items!"
    }


@app.get("/items/<id>")
def get_item(id: int):
    logger.info(f"Get item ID: {id}")
    return {
        "statusCode": 200,
        "body": "Get item!"
    }


@app.post("/items")
def create_item():
    item: dict = app.current_event.json_body
    logger.info(f"Create item: {item}")
    return {
        "statusCode": 200,
        "body": "Create item!"
    }

@app.put("/items/<id>")
def update_item(id: int):
    item: dict = app.current_event.json_body
    logger.info(f"Update item: {item} with ID: {id}")
    return {
        "statusCode": 200,
        "body": "Update item!"
    }


@app.delete("/items/<id>")
def delete_item(id: int):
    logger.info(f"Delete item ID: {id}")
    return {
        "statusCode": 200,
        "body": "Delete item!"
    }


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
def handler(event: dict, context: LambdaContext) -> dict:
    logger.info(f" Event: {event}")
    return app.resolve(event, context)
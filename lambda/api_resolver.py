from aws_lambda_powertools import Logger
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext
from aws_lambda_powertools.event_handler import APIGatewayRestResolver

logger = Logger()
app = APIGatewayRestResolver()

@app.get("/tasks")
def get_tasks() -> dict:
    return {
        "statusCode": 200,
        "body": "Get all tasks!"
    }


@app.get("/task/<id>")
def get_task(id: int) -> dict:
    logger.info(f"Get task ID: {id}")
    return {
        "statusCode": 200,
        "body": "Get item!"
    }


@app.post("/task")
def create_task() -> dict:
    task: dict = app.current_event.json_body
    logger.info(f"Create task: {task}")
    return {
        "statusCode": 200,
        "body": "Create item!"
    }

@app.put("/task/<id>")
def update_tasks(id: int) -> dict:
    item: dict = app.current_event.json_body
    logger.info(f"Update task: {item} with ID: {id}")
    return {
        "statusCode": 200,
        "body": "Update task!"
    }


@app.delete("/task/<id>")
def delete_tasks(id: int) -> dict:
    logger.info(f"Delete task ID: {id}")
    return {
        "statusCode": 200,
        "body": "Delete task!"
    }


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
def handler(event: dict, context: LambdaContext) -> dict:
    logger.info(f" Event: {event}")
    return app.resolve(event, context)
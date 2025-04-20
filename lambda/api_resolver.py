from aws_lambda_powertools import Logger
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
import boto3

logger = Logger()
app = APIGatewayRestResolver()

# Get a connection to DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('tasker-api-table')

@app.get("/tasks")
def get_tasks() -> dict:
    # Get all tasks from DynamoDB
    logger.info("Get all tasks")
    try:
        response = table.scan()
        tasks = response.get('Items', [])
        logger.info(f"Tasks retrieved: {tasks}")
    except Exception as e:
        logger.error(f"Error retrieving tasks: {e}")
        return {
            "statusCode": 500,
            "body": "Error retrieving tasks"
        }
    # Return the tasks
    if not tasks:
        return {
            "statusCode": 404,
            "body": "No tasks found"
        }
    # Return the tasks in the response
    return {
        "statusCode": 200,
        "body": tasks
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

    # Ensure the task has a valid primary key
    if "id" not in task:
        return {
            "statusCode": 400,
            "body": "Task must include an 'id' field."
        }

    # Add the task to DynamoDB
    try:
        table.put_item(Item=task)
        logger.info(f"Task created: {task}")
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        return {
            "statusCode": 500,
            "body": "Error creating task"
        }
    return {
        "statusCode": 201,
        "body": "Task created!"
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

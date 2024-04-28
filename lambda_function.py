import os
import json
import boto3
import traceback

from aws_lambda_powertools.logging import Logger
from aws_lambda_powertools.event_handler.api_gateway import ApiGatewayResolver

from services.user_service import UserService

client_id = os.environ["client_id"]
region_name = os.environ["region_name"]
user_pool_id = os.environ["user_pool_id"]

cognito_client = boto3.client("cognito-idp", region_name=region_name)
user_service = UserService(client_id, cognito_client)

logger = Logger(service=user_pool_id)
logger.set_correlation_id(client_id)

resolver = ApiGatewayResolver()


@resolver.route("/user", methods=["POST"])
def lambda_handler(event: dict, context):
    try:
        body: dict = event["body"]

        logger.info(f"Payload: {json.dumps(body)}")

        cpf: str = body["cpf"]
        password: str = body["password"]

        if event["path"] == "/user/create":
            response = user_service.create_user(cpf, password)
            logger.info(response["body"])
            return response
        elif event["path"] == "/user/authenticate":
            response = user_service.authenticate_user(cpf, password)
            logger.info(response["body"])
            return response
        else:
            return {"statusCode": 400, "body": json.dumps({"error": "Rota inválida."})}
    except Exception as ex:
        logger.error(ex)
        logger.error(traceback.format_exc())

        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Erro desconhecido, favor analisar os logs."}),
        }

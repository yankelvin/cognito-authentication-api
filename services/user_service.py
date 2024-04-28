import json


class UserService:
    def __init__(self, client_id, cognito_client) -> None:
        self.client_id = client_id
        self.cognito_client = cognito_client

    def create_user(self, username, password):
        try:
            response = self.cognito_client.sign_up(
                ClientId=self.client_id, Username=username, Password=password
            )
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "Usuário criado com sucesso"}),
            }
        except self.cognito_client.exceptions.UsernameExistsException:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "O usuário já existe."}),
            }
        except Exception as e:
            return {
                "statusCode": 500,
                "body": json.dumps(
                    {"error": f"Ocorreu um erro ao criar o usuário: {e}"}
                ),
            }

    def authenticate_user(self, username, password):
        try:
            response = self.cognito_client.initiate_auth(
                AuthFlow="USER_PASSWORD_AUTH",
                AuthParameters={"USERNAME": username, "PASSWORD": password},
                ClientId=self.client_id,
            )
            return {"statusCode": 200, "body": json.dumps(response)}
        except self.cognito_client.exceptions.NotAuthorizedException:
            return {
                "statusCode": 401,
                "body": json.dumps({"error": "Usuário ou senha inválidos."}),
            }
        except Exception as e:
            return {
                "statusCode": 500,
                "body": json.dumps(
                    {"error": f"Ocorreu um erro ao autenticar o usuário: {e}"}
                ),
            }

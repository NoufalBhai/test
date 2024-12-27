import os
import jwt
import requests
from jwt.exceptions import InvalidTokenError

USER_POOL_ID = os.environ['USER_POOL_ID']
REGION = os.environ['REGION']

# Cognito JWKS URL
JWKS_URL = f"https://cognito-idp.{REGION}.amazonaws.com/{USER_POOL_ID}/.well-known/jwks.json"
jwks = requests.get(JWKS_URL).json()

def verify_token(token):
    """
    Verifies the JWT token using Cognito's JWKS keys.
    """
    try:
        headers = jwt.get_unverified_header(token)
        key = next((k for k in jwks['keys'] if k['kid'] == headers['kid']), None)
        if not key:
            raise InvalidTokenError("Public key not found.")

        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)
        decoded = jwt.decode(
            token,
            key=public_key,
            algorithms=['RS256'],
            audience=os.environ['RESOURCE_SERVER_IDENTIFIER'],
            issuer=f"https://cognito-idp.{REGION}.amazonaws.com/{USER_POOL_ID}"
        )
        return decoded
    except InvalidTokenError as e:
        raise Exception(f"Token verification failed: {str(e)}")

def handler(event, context):
    """
    Lambda function handler for API Gateway requests.
    """
    token = event['headers'].get('Authorization', '').replace('Bearer ', '')
    if not token:
        return {"statusCode": 401, "body": "Unauthorized"}

    try:
        user = verify_token(token)
        return {
            "statusCode": 200,
            "body": "Access granted with valid token and scope."
        }
    except Exception as e:
        return {
            "statusCode": 403,
            "body": str(e)
        }

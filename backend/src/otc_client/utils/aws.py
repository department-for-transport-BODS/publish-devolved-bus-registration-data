import boto3
import json
from botocore.exceptions import ClientError
from os import getenv

import logging

logging.basicConfig(format="%(levelname)s,%(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, getenv("LOG_LEVEL", "INFO")))


def get_secret(secret_arn: str) -> str:
    """
    Retrieves the value of a secret specified by its ARN.

    Parameters:
    secret_arn (str): The ARN/Name of the secret to retrieve.

    Returns:
    str: The value of the retrieved secret.
    """
    session = boto3.session.Session()
    client = boto3.client(
        service_name="secretsmanager",
        region_name=getenv("AWS_REGION"),
    )
    try:
        response = client.get_secret_value(SecretId=secret_arn)
        logger.info("The specified secret was successfully retrieved")
        return json.loads(response["SecretString"])
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            logger.error("The specified secret was not found")
        else:
            logger.error(f'The error "{e}" occurred when retrieving the secret')
        raise Exception(e)

# Content to create
import os
import boto3

def get_secret(name: str) -> str:
    if os.getenv("ENV") == "prod":
        return boto3.client('secretsmanager').get_secret_value(SecretId=name)['SecretString']
    return os.getenv(name.upper())
import boto3
import os
import psycopg2
from .logger import log

def connect_to_db():
    # Connect to the database
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('your_table_name')
    
    return table

def get_results_db_conn():
    conn = None
    environment = os.environ.get("ENVIRONMENT", "local")
    log.debug(f"env: {environment}")
    if environment != "local":
        log.info("Using argo environment")
        aws_region = os.getenv("REGION", "eu-west-1")
        session = boto3.session.Session()
        rds = session.client(service_name="rds", region_name=aws_region)
        os.environ["DB_TOKEN"] = rds.generate_db_auth_token(
            DBHostname=os.environ.get("DB_HOST"),
            Port=int(os.environ.get("DB_PORT")),
            DBUsername=os.environ.get("DB_USER"),
            Region=aws_region,
        )
    log.info(f'Automation host: {os.environ.get("DB_HOST")}')
    log.info(f'Automation port: {os.environ.get("DB_PORT")}')
    log.info(f'Automation user: {os.environ.get("DB_USER")}')
    log.info(f'Automation DB: {os.environ.get("DB_DATABASE")}')
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=os.environ.get("DB_PORT", "5432"),
        database=os.environ.get("DB_DATABASE", "postgres"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_TOKEN", "postgres"),
    )
    if conn is not None:
        print("Connection established to PostgreSQL.")
    else:
        print("Connection not established to PostgreSQL.")
    return conn


def create_item(table, item):
    # Create a new item in the database
    response = table.put_item(Item=item)
    return response

def read_item(table, key):
    # Read an item from the database
    response = table.get_item(Key=key)
    item = response.get('Item')
    return item

def update_item(table, key, update_expression, expression_attribute_values):
    # Update an item in the database
    response = table.update_item(
        Key=key,
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values
    )
    return response

def delete_item(table, key):
    # Delete an item from the database
    response = table.delete_item(Key=key)
    return response

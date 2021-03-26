import json
import os
import decimalencoder
from db import get_session,Todo,AlchemyEncoder
import boto3

def list(event, context):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch all entries from the database
    result = table.scan()

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'], cls=decimalencoder.DecimalEncoder),
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true"
        }
    }

    return response

def list_mysql(event, context):
    session = get_session()
    todos = session.query(Todo).all()
    response = {
        "statusCode": 200,
        "body": json.dumps(todos, cls=AlchemyEncoder),
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true"
        }
    }

    return response
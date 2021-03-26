import json
import os
from db import get_session,Todo,AlchemyEncoder
import boto3
import decimalencoder

def get(event, context):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch a person from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'], cls=decimalencoder.DecimalEncoder),
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true"
        }
    }

    return response

def get_mysql(event, context):
    session = get_session()
    todo_id = event['pathParameters']['id']
    todo = session.query(Todo).filter_by(id=todo_id).one()

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(todo, cls=AlchemyEncoder),
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true"
        }
    }

    return response   
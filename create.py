import json
import os
import time
import uuid
from db import get_session,Todo,AlchemyEncoder
import sqlalchemy
import boto3

def create(event, context):
    dynamodb = boto3.resource('dynamodb')

    data = json.loads(event['body'])

    timestamp = int(time.time() * 1000)

    # Creating a table inside DynamoDB
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # Items to populate the table
    item = {
        'id': str(uuid.uuid1()),
        'firstName': data['firstName'],
        'lastName': data['lastName'],
        'email': data['email'],
        'comments': data['comments'],
        'options': data['options'],
        'checked': False,
        'createdAt': timestamp,
        'updatedAt': timestamp
    }

    # write the item to the database
    table.put_item(Item=item)

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item),
        "headers": {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Credentials": "true"
        }
    }

    return response

def create_mysql(event, context):
    data = json.loads(event['body'])
    timestamp = sqlalchemy.sql.func.now()

    newTodo = Todo(
        id= str(uuid.uuid1()),
        firstName= data['firstName'],
        lastName= data['lastName'],
        email= data['email'],
        comments= data['comments'],
        options= data['options'],
        checked= False,
        createdAt= timestamp,
        updatedAt= timestamp
    )
    session = get_session()
    session.add(newTodo)
    session.commit()

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(newTodo, cls=AlchemyEncoder),
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true"
        }
    }

    return response   

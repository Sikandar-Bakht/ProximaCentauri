import os 
import boto3
import json
from S3bucket import S3Bucket as sb
import botocore
from boto3.dynamodb.conditions import Attr

TABLE_PATH = '/TABLE'
BUCKET_PATH = '/BUCKET_LIST'

def lambda_handler(event, context):
    
    path = event['path']
    httpMethod = event['httpMethod']
    origin = None
    if origin in event['headers']:
        origin = event['headers']['origin']
    body = event['body']
    table_name = os.getenv("api_table_name")
    print(event)
    response = {}
    if path == BUCKET_PATH and httpMethod == 'PUT':
        
        bucket_name = event['queryStringParameters']["bucket_name"]
        object_key = event['queryStringParameters']["object_key"]
        response = bucket_to_table(bucket_name, object_key, table_name, origin)
        
    elif path == TABLE_PATH and httpMethod == 'GET':
        
        if event['queryStringParameters'] is not None:
            url = event['queryStringParameters']['url']
            response = fetch_url(table_name, origin, url)
            print(response, origin)
        else:
            response = fetch_url(table_name, origin)
        
    elif path == TABLE_PATH and httpMethod == 'POST':
        
        url_name = event['queryStringParameters']['url_name']
        new_url = event['queryStringParameters']['url']
        
        response = add_url(table_name, url_name, new_url)
        
    elif path == TABLE_PATH and httpMethod == 'PUT':
        
        url_to_update = event['queryStringParameters']['url']
        url_name = event['queryStringParameters']['url_name']
        
        body = json.loads(event['body'])
        updated_url_name = body['updated_url_name']
        updated_url = body['updated_url']
        response = update_url(table_name, url_name, url_to_update, updated_url_name, updated_url)
    
    elif path == TABLE_PATH and httpMethod == 'DELETE':
        
        print(event)
        url_name = event['queryStringParameters']['url_name']
        url_del = event['queryStringParameters']['url']
        response = delete_url(table_name, url_name, url_del)   

    else:
        print(event)
        response = {
                    "statusCode":300,
                    "headers": {
                                "Access-Control-Allow-Headers" : "application/json",
                                "Access-Control-Allow-Origin": "*",
                                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                               },
                    "body": "request failed"
                    }
   
    return response


def construct_response(msg, origin=None):
    
    if origin is None:
        response = {
                "statusCode":200,
                "headers": {
                                "Access-Control-Allow-Headers" : "application/json",
                                "Access-Control-Allow-Origin": "*",
                                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                               },
                "body": msg
               }
    else:
        response = {
                "statusCode":200,
                "headers": {
                                "Access-Control-Allow-Headers" : "application/json",
                                "Access-Control-Allow-Origin": origin,
                                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                               },
                "body": msg
               }
    return response


def bucket_to_table(bucket_name, object_key, table_name, origin):
    '''
    
    RESPONSE OF LOADING URLS FROM BUCKET
    
    inputs:
    bucket_name (str): Name of S3 bucket_to_table
    object_key (str): Name of object file in S3 bucket_to_table
    table_name (str): name of table
    
    returns: 
    (dict) contains status code and a message
    
    '''
    
    URLS = sb(bucket_name).load(object_key)
    K=list(URLS['URLS'][0].keys())
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    for i in range(len(K)):
        table.put_item(Item = {
                                'URL': URLS['URLS'][0][K[i]],
                                'Name': K[i]})
    
    msg = f"{len(K)} urls added/updated"
    return construct_response(msg, origin)



def fetch_url(table_name, origin, url=None):
    '''
    
    RESPONSE OF READING URLS FROM TABLE
    
    inputs:
    url (str): url specified by key
    table_name (str): name of table
    
    returns: 
    (dict) contains status code and a message
    
    '''
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    if url is not None:
        URL = table.get_item(Key = {'URL': url})
        
        if 'Item' in URL:
           # msg = URL['Item']['Name'] + ": " + URL['Item']['URL'] 
           msg = f'''
                    "Name": {URL['Item']['Name']},
                    "URL": {URL['Item']['URL']}
                    
                 '''
        else:
            msg = "Specified URL name does not exist"
        
    else:
        response = table.scan()
        URL = response['Items']
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            URL.extend(response['Items'])
        
        msg = []
        for i in range(len(URL)):
            msg.append({
                        "Name": URL[i]['Name'],
                        "URL": URL[i]['URL']
                      })
                    
    return construct_response(json.dumps(URL), origin)
        
        


def add_url(table_name, url_name, new_url):
    '''
    
    RESPONSE OF ADDING URLS TO TABLE
    
    inputs:
    url_name (str): Name given to a url. 
    new_url (str): New url to be added to the table
    table_name (str): name of table
    
    returns: 
    (dict) contains status code and a message
    
    '''
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    try:
        table.put_item (Item = {'URL': new_url,
                                'Name' : url_name
                              },
                        ConditionExpression=Attr('URL').ne(new_url)
                        )
        msg = f'''
            URL Name: {url_name}
            URL: {new_url}
        '''               
        
    except botocore.exceptions.ClientError as e:
    
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            
            msg = f'URL: {new_url} already exists'
            
    return construct_response(msg)

    
def delete_url(table_name, url_name, url_del):
    
    '''
    
    RESPONSE OF UPDATING URLS IN TABLE
    
    inputs:
    url_name (str): Name given to a url.
    url_del (str): Url to delete from table
    table_name (str): name of table
    
    returns: 
    (dict) contains status code and a message
    
    '''    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    try:
        table.delete_item (Key = {'URL': url_del,
                              },
                        ConditionExpression=Attr('URL').eq(url_del)
                        )
        msg = f'''
            Deleted
            URL Name: {url_name}
            URL: {url_del}
        '''               
        
    except botocore.exceptions.ClientError as e:
    
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            
            msg = f'URL: {url_del} does not exist'
            
    return construct_response(msg)
    
def update_url(table_name, url_name, url_to_update, updated_url_name, updated_url):
    
    '''
    
    RESPONSE OF ADDING URLS TO TABLE
    
    inputs:
    url_name (str): Name given to a url. Defaults to 'Unknown'
    url_to_update (str): Url that needs to be updated
    updated_url_name (str): Name given to an updated url. Defaults to 'Unknown'
    updated_url (str): Url that is updated to
    table_name (str): name of table
    
    returns: 
    (dict) contains status code and a message
    
    '''

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    msg = ''
    
    try:
        table.delete_item (Key = {'URL': url_to_update,
                              },
                        ConditionExpression=Attr('URL').eq(url_to_update)
                        )
        
    except botocore.exceptions.ClientError as e:
    
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            
            msg = f'URL: {url_to_update} does not exist'
    
    if msg != f'URL: {url_to_update} does not exist':
        try:
            table.put_item (Item = {'URL': updated_url,
                                    'Name' : updated_url_name
                                  },
                            ConditionExpression=Attr('URL').ne(updated_url)
                            )
            msg = f'''
            Update from:
                URL: {url_to_update}
                URL Name: {url_name}
            to:  
                URL Name: {updated_url_name}
                URL: {updated_url}
            '''               
            
        except botocore.exceptions.ClientError as e:
        
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                msg = f'URL: {updated_url} already exists S'
            
    return construct_response(msg)
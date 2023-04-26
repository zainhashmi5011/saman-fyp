import jwt
import requests

def encode_token (object):
    payload = {
        'id':object.id,
        'email':object.email,
        'user_type':object.user_type,
    }
    secret_key = "cancerclarity"

    token = jwt.encode(payload,secret_key, algorithm= "HS256")
    if token:
        return token
    return None 
    

def social_auth_token(payload):
    print(payload)
    secret_key = "cancerclarity"
    token = jwt.encode(payload,secret_key,algorithm="HS256")
    return token if token else None

def create_response(error , message , data =[] ):
    kwargs = {
        "error" : error,
        "message" : message,
        "data" : data
    }
    return kwargs

def decode_token(token):
    secret_key = "cancerclarity"
    payload = jwt.decode(token, secret_key, algorithms="HS256")
    return payload

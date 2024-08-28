import os
import base64
from functools import wraps
from azure.functions import HttpRequest, HttpResponse


def basic_auth():
    def decorator(func):
        @wraps(func)
        def wrapper(req: HttpRequest, *args, **kwargs):
            auth_header = req.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Basic '):
                return HttpResponse("Unauthorized", status_code=401)

            encoded_credentials = auth_header.split(' ')[1]
            decoded_credentials = base64.b64decode(
                encoded_credentials).decode('utf-8')
            request_username, request_password = decoded_credentials.split(':')

            username = os.getenv('BASIC_AUTH_USERNAME')
            password = os.getenv('BASIC_AUTH_PASSWORD')

            if request_username == username and request_password == password:
                return func(req, *args, **kwargs)
            else:
                return HttpResponse("Unauthorized", status_code=401)
        return wrapper
    return decorator

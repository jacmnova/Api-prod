import time

from jwt import encode, decode
from jwt import exceptions
from os import getenv
from datetime import datetime, timedelta
import datetime
from flask import jsonify


access_token = ''

def set_token(token):
    global access_token
    access_token = token
    return

def get_token_data():
    data = validate_token(access_token, True)
    return data

def expire_date(days: int):
    now = datetime.datetime.now()
    new_date = now + timedelta(days)
    return new_date

def expire_min():
    now = datetime.now()
    new_date = now + timedelta(days=0, minutes=10)
    print(new_date, 'EXPIRED TOKEN')
    return new_date

def write_token_web(data: dict):
    token = encode(payload={**data, "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=1800)}, key="zsqwk#zoTncp7k%zfOnS3CnSc$&Nv16eEWnBgz51K4fTwBOZ9V", algorithm="HS256")
    print(token)
    # validate_token(token.encode("UTF-8"), True)
    return token.encode("UTF-8")

def write_token(data: dict, days):
    token = encode(payload={**data, "exp": expire_date(days)}, key="zsqwk#zoTncp7k%zfOnS3CnSc$&Nv16eEWnBgz51K4fTwBOZ9V", algorithm="HS256")
    return token.encode("UTF-8")

def validate_token(token, output=False):
    # if output:
    #     return decode(token, key="zsqwk#zoTncp7k%zfOnS3CnSc$&Nv16eEWnBgz51K4fTwBOZ9V", algorithms=["HS256"])
    # else:
    #     decode(token, key="zsqwk#zoTncp7k%zfOnS3CnSc$&Nv16eEWnBgz51K4fTwBOZ9V", algorithms=["HS256"])
    try:
        if output:
            return decode(token, key="zsqwk#zoTncp7k%zfOnS3CnSc$&Nv16eEWnBgz51K4fTwBOZ9V", algorithms=["HS256"] )
        else:
            decode(token, key="zsqwk#zoTncp7k%zfOnS3CnSc$&Nv16eEWnBgz51K4fTwBOZ9V", algorithms=["HS256"])
    except exceptions.DecodeError:
        response = jsonify({"message": "Invalid Token"})
        response.status_code = 401
        return response
    except exceptions.ExpiredSignatureError:
        response = jsonify({"message": "Token Expired"})
        response.status_code = 401
        return response

def refresh_token(token):
    print("Renovando token de sesion")
    info_token = validate_token(token, True)
    print(info_token)
    new_token = write_token_web(info_token)
    print(new_token)
    return str(new_token).split("'")[1]

from medic.const import ERROR_API_KEY
from medic.models import AuthenticationData
from flask import request

def identy_token(func):
    def substitution(*argv, **kwargs):
        if AuthenticationData.check_token(request.headers.get('Authorization', default="")):
            return func(argv, **kwargs) 
        else: return {"message":ERROR_API_KEY}, 401
        
    return substitution

def get_identy():
        user = AuthenticationData.check_token(request.headers.get('Authorization', default=""))
        return user
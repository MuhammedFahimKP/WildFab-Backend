from urllib.parse import parse_qs
from datetime import datetime


from channels.exceptions import DenyConnection
from channels.middleware import BaseMiddleware

from channels.db import database_sync_to_async


from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken

from django.contrib.auth import get_user_model


from django.conf import settings



USER = get_user_model()


class BaseJWTAuthMiddleWare(BaseMiddleware):
    
    controller_ws_paths = ['user','admin']
    
    async def __call__(self, scope, receive, send):
        """
        ASGI application; can insert things into the scope and run asynchronous
        code.
        """
        
        
    
        
        # Copy scope to stop changes going upstream
        scope = dict(scope)
        
        
        
        querparams = self.processed_query_params(scope['query_string'])
        
        
        
        token  = querparams.get('token')
        
        exceptions = dict()
        
        if token is None:
           
            exceptions['code'] = 4001
            exceptions['reason'] = 'Token Missing in Query String'

        else :
            
            user_id = await self.get_user_from_token(token)
            
            if user_id is None :
                    
                exceptions['code'] = 4001
                exceptions['reason'] = 'Token Expired'
            
            
            else :
                
                scope['user'] = user_id    
                
                    
                        
            
        if len(exceptions.keys())  == 2 :
            
            scope['error'] = exceptions
            
        
    
            
        return  await self.inner(scope,receive,send)  
        
    
    
    
         
        
        
    
    
    
    @database_sync_to_async
    def get_user_from_token(self, token):
            try:
                access_token = AccessToken(token)
                return access_token['user_id']
            except:
                return None
    
    
    
    
    
    @staticmethod
    def processed_query_params(bytstring_param) :
        
        decoded_string = bytstring_param.decode('utf-8')

        #  Parse the query string into a dictionary
        # parse_qs returns a dictionary where the values are lists, use {k: v[0]} to get single values
        parsed_dict = {k: v[0] for k, v in parse_qs(decoded_string).items()}
        
        return parsed_dict
    
    

  
    
    
    
    
    
    
        


class PathAuthMiddleware:
    def __init__(self, app):
        self.controller_app = BaseJWTAuthMiddleWare(app)
        self.other_app      = BaseMiddleware(app)
    
    async def __call__(self, scope, receive, send):
                
        path = scope['path'].split('/')[1]    
        
        if path in BaseJWTAuthMiddleWare.controller_ws_paths:
            return await self.controller_app(scope, receive, send)
        return self.other_app(scope, receive, send)  
    
    
    

    
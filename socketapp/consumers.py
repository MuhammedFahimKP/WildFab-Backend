
import json

from django.contrib.auth import get_user_model

from asgiref.sync import async_to_sync,sync_to_async


from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from shop.models import Cart,WishList
from manager.utils import get_count_of_admin_data





USER = get_user_model()



class BaseJWTAuthConsumer(AsyncWebsocketConsumer):
    
    
    
    
    
    async def connect(self):
        
        return super().connect()
    
    
    
    async def authenticate(self):
        
        user_id =  self.scope.get('user',None)
        
        
        if user_id is not None :
            
            user = await self.get_user(user_id=user_id)  
            
            
            if  user not in [None , False] :
                
                return user 
            
            return False
        
        else :
            return None
    
    
    
     
        
          
        
    
    async def disconnect(self, code,message=''):        
        return await self.close(code,reason=message)
    
    
    

    
    
    
    def auth_error_occured(self):    
        return 'auth_error' in self.scope  
        
    

    @database_sync_to_async    
    def get_user(self,user_id):
    
            
        try :
            user = USER.objects.get(id=user_id)
            
            if user.is_active == False:            
                
                
                self.scope['auth_error'] = {
                    'code':4001, 
                    'reason':'Not A Verfied User', 
                }               
                
                return False               
            
            
              
    
            
            return user
        
            
                
                
        
        except USER.DoesNotExist :
            
            self.scope['auth_error'] = {
                'code':4004,
                'reason':'user not found',
            }
            
            return None       
        
    def is_error_exists(self):
        """This checks if error exists during websockets"""

        return True if 'error' in self.scope else False
                 
    
    
    
    
    async def send_message(self,data):
        return  await self.send(text_data=json.dumps(data))
    
    
    async def disconnect(self, code, reason =''):
        
    
        if hasattr(self,'user_loged') :
            
            
            async_to_sync(self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            ))
        
        
        
        
        await self.send_message({'code':code ,'reason':reason } )    
        await self.close()     
        
    


class BaseJWTAdminAuthConsumer(BaseJWTAuthConsumer):
    
    
    async def get_user(self,user_id):
        user = await super().get_user(user_id)
        
        if user is not None or user != False:
            
            if user.is_staff == False  or user.is_superuser  == False :
                
                self.scope['auth_error'] = {
                    'code':4001, 
                    'reason':'Wrong User Type Excpted An Admin User', 
                }               
                
                return False 
            
    
        return user     

            
class GetCartAndWishlistCountConsumer(BaseJWTAuthConsumer) :
    
    
    async def accept(self, subprotocol=None, headers=None):
        
        return await super().accept(subprotocol, headers)
    
    
    
    
    
    
    
    
    
    async def connect(self):
        
        
        await self.accept()
        await self.get_count() 
               
        
    
    
    
        
             
                

         
                
        
    
    
    
    
    @database_sync_to_async
    def get_whislist_cartcount(self,user):
        
        
        cart           = Cart.objects.filter(user=user)
        wishlist       = WishList.objects.filter(user=user)
        cart_items     = 0     
        wishlist_items = 0 
        
               
        if cart.exists():
            
            
            cart       = cart.first()
            cart_items = cart.cart_items.all().count()
        
        
        if wishlist.exists():
            
            wishlist = wishlist.first()
            wishlist_items = wishlist.wishlist_items.all().count()
                
        
        
        
        
        return {
            'cart':cart_items,
            'wishlist':wishlist_items
        }
        
        
        
    
    
    async def get_count(self):
    
        user =  self.scope['user']
        
        data = await self.get_whislist_cartcount(user)
        
        
        await self.send_message(data=data) 
    
    
      
    
    
    
    async def send_notification(self, event):
        
        
        data = event.get('data',None)
        
        if data is not None:
            await self.send_message(data=data)   
            
    
class AdminDashBoardCountConsumer(BaseJWTAuthConsumer):
            
        
            

        
    
    
    async def connect(self):
        
        await self.accept()
        
        
        if self.is_error_exists() :
            
           await self.send_message(self.scope['error'])
           await self.close()
        
        
           
           
        else :
            await self.get_count()
            
            
    
    async def get_count(self):
        
        
        user = self.scope.get('user',None)
        
        
        if user is not None :
            
            user = await self.get_user(user)
            
            
            
            
            
            
            if user is not None:
                
                
                if user.is_active == False:
                    
                    await self.disconnect(code=4001,reason='not a verfied user')
                
                if user.is_superuser and  user.is_staff:
                    
                    self.user_loged = True
                    
                    self.group_name = 'admins_dashboard_count'
                    
                    
                    await self.channel_layer.group_add(
                        self.group_name,
                        self.channel_name
                    )
                    
                    data = await sync_to_async(get_count_of_admin_data)()
                    
                    
                
                    
                    
                    await self.send_message(data)
                    
                
                
                else :    
                    await self.disconnect(code=4001,reason='unauthoride only admin users have access')  
                    
            else :
                await self.disconnect(code=4004,reason='user not found')        
                    
        else:
            
            await self.disconnect(code=4001,reason='no user')    
            
            
            
    async def send_notification_admin(self,event):
        data = await sync_to_async(get_count_of_admin_data)()     
        await self.send_message(data=data) 
        
         
                
                
# class AdminDashBoardSalesData(BaseJWTAuthConsumer):
    
    
    
    
        
            

        
    
    
#     async def connect(self):
        
#         await self.accept()
        
        
#         if self.is_error_exists() :
            
#            await self.send_message(self.scope['error'])
#            await self.close()
           
           
#         else :
#             await self.get_count()
            
            
    
#     async def get_count(self):
        
        
#         user = self.scope.get('user',None)
        
        
#         if user is not None :
            
#             user = await self.get_user(user)
            
            
            
            
            
            
#             if user is not None :
                
                
#                 if user.is_active == False:
                    
#                     await self.disconnect(code=4001,reason='not a verfied user')
                
#                 if user.is_superuser and  user.is_staff:
                    
#                     self.user_loged = True
                    
#                     self.group_name = 'admins_dashboard_count'
                    
                    
#                     await self.channel_layer.group_add(
#                         self.group_name,
#                         self.channel_name
#                     )
                    
#                     data = await sync_to_async(get_count_of_admin_data)()
                    
                    
                
                    
                    
#                     await self.send_message(data)
                    
                
                
#                 else :    
#                     await self.disconnect(code=4001,reason='unauthoride only admin users have access')  
                    
#             else :
#                 await self.disconnect(code=4004,reason='user not found')        
                    
#         else:
            
#             await self.disconnect(code=4001,reason='no user')    
                     
            
                
                
                
                
            
        
        
    
                
            
        
        
    
    
             
            
           


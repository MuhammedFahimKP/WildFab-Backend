from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete
from .models import (
    CartItem,
    WishListItem,
    Product,
    Brand,
)
from .utils import get_count_wishlist_cart
from utils.wsocket import group_send




@receiver([post_save,post_delete], sender=Brand)
def brand_count_handler(sender, instance,signal,created=False, **kwargs):
    
    
    print(signal)

    group_name  = "admins_dashboard_count"
    send_method = 'send_notification_admin'
    
    if signal == post_save: 
       
       if created:
           group_send(group_name,send_method,data={})
         
    
    if signal == post_delete :
        group_send(group_name,send_method,data={})    





@receiver([post_save,post_delete], sender=Product)
def product_count_handler(sender, instance,signal,created=False, **kwargs):
    

    group_name  = "admins_dashboard_count"
    send_method = 'send_notification_admin'
    
    if signal == post_save: 
       
       if created:
           group_send(group_name,send_method,data={})
         
    
    if signal == post_delete :
        group_send(group_name,send_method,data={})    






@receiver([post_save,post_delete], sender=CartItem)
def cart_count_handler(sender, instance,signal,created=False, **kwargs):

    user = instance.cart.user
    group_name = f"{user.id}s_cart_wishlist"
    
    send_method = 'send_notification'
    
    if signal == post_save: 
       
       if created :
           
           data  = get_count_wishlist_cart(user)
           
           group_send(group_name,send_method,data=data)
         
    
    if signal == post_delete :
        data = get_count_wishlist_cart(user)
        group_send(group_name,send_method,data=data)       
           
       
        
        
    
    
@receiver([post_save,post_delete], sender=WishListItem)
def wishlist_count_handler(sender, instance,signal,created=False, **kwargs):
    
    user = instance.wishlist.user
    group_name = f"{user.id}s_cart_wishlist"
    
    send_method = 'send_notification'
    
    if signal == post_save: 
       
       if created :
           
           data  = get_count_wishlist_cart(user)
           
           group_send(group_name,send_method,data=data)
         
    
    if signal == post_delete :
        data = get_count_wishlist_cart(user)
        group_send(group_name,send_method,data=data)    
        
            
    
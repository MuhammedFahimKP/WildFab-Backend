from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete

from utils.wsocket import group_send

from .models import Order



@receiver([post_save,post_delete], sender=Order)
def order_count_handler(sender, instance,signal,created=False, **kwargs):
    

    group_name  = "admins_dashboard_count"
    send_method = 'send_notification_admin'
    
    if signal == post_save: 
       
       if created:
           group_send(group_name,send_method,data={})
  
    
    
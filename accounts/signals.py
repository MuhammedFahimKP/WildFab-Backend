from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete

from django.contrib.auth import get_user_model

from utils.wsocket import group_send





USER = get_user_model()






@receiver([post_save,post_delete], sender=USER)
def user_count_handler(sender, instance,signal,created=False, **kwargs):
    

    group_name  = "admins_dashboard_count"
    send_method = 'send_notification_admin'
    
    if signal == post_save: 
       
       if created:
           group_send(group_name,send_method,data={})
         
    
    if signal == post_delete :
        group_send(group_name,send_method,data={})    

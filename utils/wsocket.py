from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def group_send(group_name,send_method,data):
    
    """
    
    group name  : name of the group
    
    sender_method : name of method in  particualar group consumer
    
    data : data to send to the consumer
    
    """
    
    
    try :
    
    
        channel_layer= get_channel_layer()
        
        async_to_sync(channel_layer.group_send)(group_name,{
            'type':send_method,
            'data':data,
        })
        
    
    except Exception as e :
        
        print(e)
        
        pass


 

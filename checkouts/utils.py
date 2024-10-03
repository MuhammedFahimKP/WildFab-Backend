from decimal import Decimal

import razorpay

from django.conf import settings

from django.db.models import Count
from django.db.models.functions import TruncDay


from datetime import datetime



from .models import Order






class RazorPay:
    
    
    client = razorpay.Client(auth=(settings.RAZOR_PAY_KEY,settings.RAZOR_PAY_SECRETE_KEY))
        
    
        


    
    
    
    
    
    @classmethod
    def create_payment_order(cls,amount:Decimal,currency:str) -> dict:
        
        data = {
            
            'amount':float(amount) *100,
            'currency':currency,
        }
    
        
        payment_order = cls.client.order.create(data=data)
        return payment_order
    
    @classmethod
    def verfiy_payment(cls,order_id:str,payment_id:str,signature:str) -> dict:
        
    
        
        data = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        
        try :
            check = cls.client.utility.verify_payment_signature(data)
            return check 
        
        except razorpay.errors.SignatureVerificationError:
            pass
        
        return False
             
        
    


def calculate_gst(amount:float) -> float:
    return amount * 0.12    


 

def get_order_count_for_dashboard(year=None,month=None) :   
    
    year_to_filter  = year  if year  else datetime.now().strftime("%Y")
    month_to_filter = month if month else datetime.now().strftime("%m").lstrip('0')
    
    
    
    
    orders = Order.objects.filter(
    
        created__year=year_to_filter,
        created__month=month_to_filter,
        payment_status='Paid'
    )
        
        
    sales_data = (
        orders
        .annotate(day=TruncDay('created'))
        .values('day')
        .annotate(order_count=Count('id'))
        .order_by('day')
    )

     
    #formating data in the form of count and orderd day of month  
    formatted_data = [
        {"day": entry["day"].day, "order_count": entry["order_count"]}
        for entry in sales_data
    ] 
    
    return formatted_data
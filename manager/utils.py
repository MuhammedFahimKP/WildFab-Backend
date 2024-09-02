from uuid import UUID

from django.contrib.auth import get_user_model

from django.db.models import Q


from rest_framework.exceptions import NotFound


from shop.models import Brand,Product


from checkouts.models import Order



USER = get_user_model()


def is_valid_uuid(uuid_to_test, version=4):
    """
    Check if uuid_to_test is a valid UUID.
    
     Parameters
    ----------
    uuid_to_test : str
    version : {1, 2, 3, 4}
    
     Returns
    -------
    `True` if uuid_to_test is a valid UUID, otherwise `False`.
    
     Examples
    --------
    >>> is_valid_uuid('c9bf9e57-1685-4c89-bafb-ff5af830be8a')
    True
    >>> is_valid_uuid('c9bf9e58')
    False
    """
    
    
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
        
    except ValueError:    
        raise NotFound()
            
    
    if str(uuid_obj) == uuid_to_test :
        return uuid_to_test




def get_count_of_admin_data():
    
    user_count    = USER.objects.count()
    product_count = Product.objects.filter(variants__isnull=False).count()
    brand_count   = Brand.objects.all().count()
    orders_count  = Order.objects.filter(Q(status='Placed') | Q(status='Delivered') ).count() 
    
    
    return   {

        'users':user_count,
        'products':product_count,
        'brand_count':brand_count,
        'orders_count':orders_count
        

    }
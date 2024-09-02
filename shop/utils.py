from django.core.exceptions import ObjectDoesNotExist


from .models import Cart,WishList





def get_or_none(class_model,**kwargs) -> object | None:

    #accepting models class and attributes
    try:

        
        
        instance = class_model.objects.get(**kwargs)

        #instance is get by attribute

        #then returning the instance  
        return instance
    
    #if there is no object exist by attribute

    
    except ObjectDoesNotExist:

        #then returning None

        return None    
    

def get_or_create(class_model,**kwargs) -> object:
    #accepting models class and attributes    

    try:
        
        instance = class_model.objects.get(**kwargs)
        #instance is get by attribute

    #if there is no object exist by attribute      
    except ObjectDoesNotExist:
        
        instance = class_model.objects.create(**kwargs)

        #then create  an instance by attributes

    #returning the instance
    return instance



def get_count_wishlist_cart(user):
    
    
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
        
        'wishlist':wishlist_items,
    }    
        

from django.db.models import Manager,Prefetch
from django.db.models import Subquery, OuterRef




class ProductMangers(Manager):
    
    
    
    def get_product_variant_model(self):
        
        from .models import  ProductVariant

        return ProductVariant
    
    
    
    def fetch_all_with_variants(self):
        
    
        
        PRODUCT_VARIANT_MODEL = self.get_product_variant_model()
        
            
        qs = self.all().prefetch_related(
                'categoery',
                'brand',
                Prefetch(
                    'variants',
                    queryset=PRODUCT_VARIANT_MODEL.objects.select_related(
                        'color',
                        'size',
                        'img'
                    )
                )
            ).filter(variants__isnull=False).distinct()
        return qs
    
    

    
    
    
    def get_with_variants(self,**kwargs):
        
        
        PRODUCT_VARIANT_MODEL = self.get_product_variant_model()
        
        
        
        
        #using keyword variant__ spearting variants filtering options 
        
        
        product_query_attr = {}
        varint_query_attr  = {}
        
        
       
        
        for attr, value  in kwargs.items():
            
            
            if attr.startswith('variant__'):
                
                varint_query_attr[attr.split('variant__')[1]] = value
                
                
            
            else :
                
                product_query_attr[attr] = value    
                
         
        if len(varint_query_attr.keys()) == 0 :
            
            
            
            
            product    = self.prefetch_related(
                
                Prefetch('variants',queryset=PRODUCT_VARIANT_MODEL.objects.select_related(
                    'color',
                ))
            ).get(**product_query_attr)
            
            
            first_variant = product.variants.all()[0]
            
            
            
            qs = self.prefetch_related(
                'categoery',
                'brand',
                Prefetch('variants',queryset=PRODUCT_VARIANT_MODEL.objects.select_related(
                
                    'color',
                    'size',
                    'img',
                ).filter(color__id=first_variant.color.id))
            ).get(**product_query_attr)
            
            
            
            
            
            return qs
        
        
        
        
         
        qs = self.prefetch_related(
                'categoery',
                'brand',
                Prefetch(
                    'variants',
                    queryset=PRODUCT_VARIANT_MODEL.objects.select_related(
                        'color',
                        'size',
                        'img'
                    ).filter(**varint_query_attr)
                )
            ).get(**product_query_attr)
        
        return qs 
    
    
    
    
        
        
        
        
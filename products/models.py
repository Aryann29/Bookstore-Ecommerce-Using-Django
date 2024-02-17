from django.db import models
from base.models import BaseModel
from django.core.exceptions import ValidationError

from django.utils import timezone
from accounts.models import Profile
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(BaseModel):
    category_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.category_name
    
class Product(BaseModel):
    
    seller = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='products')
    product_name = models.CharField(max_length=100)
    product_images = models.ImageField(upload_to="files/images")
    slug = models.SlugField(unique=True  , null=True , blank=True)
    category = models.ForeignKey(Category , on_delete=models.CASCADE , related_name="products")
    price = models.IntegerField()
    product_desription = models.TextField() #product_description correct
    # seller = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    
    def clean(self):
       
        if not self.seller.is_seller:
            raise ValidationError("Only sellers can list products.")
    
    def __str__(self):
        return f"{self.product_name} - {self.seller}"


class ProductImages(BaseModel):
    hotel= models.ForeignKey(Product ,related_name="images", on_delete=models.CASCADE)
    images = models.ImageField(upload_to="product_images")
    
    
    

class Cart(BaseModel):
    buyer = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='cart')
    products = models.ManyToManyField(Product, through='CartProduct')
    
   
    
    def __str__(self):
        return f"{self.buyer.user.username}'s cart q"  
        

class CartProduct(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def update_total_price(self):
        if self.product and self.quantity is not None:
            self.total_price = self.product.price * self.quantity
        else:
            self.total_price = 0.0
            
    @classmethod
    def cart_count(cls, cart):
        """
        Get the count of unique products in the given cart.
        """
        return cls.objects.filter(cart=cart).values('product').distinct().count()
    
    def save(self, *args, **kwargs):
        self.update_total_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name}"

@receiver(post_save, sender=Product)
def update_cart_products(sender, instance, **kwargs):
   
    cart_products = CartProduct.objects.filter(product=instance)
    for cart_product in cart_products:
        cart_product.update_total_price()
        cart_product.save()
        

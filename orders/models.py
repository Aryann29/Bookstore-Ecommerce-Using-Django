from django.db import models
from accounts.models import Profile
from products.models import Product
from base.models import BaseModel

class orders(BaseModel):
    buyer = models.ForeignKey(Profile, related_name='orders_as_buyer', on_delete=models.CASCADE)
    seller = models.ForeignKey(Profile, related_name='orders_as_seller', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_fulfilled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

# Create your models here.

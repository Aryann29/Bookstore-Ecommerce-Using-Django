from django import template
from products.models import CartProduct  

register = template.Library()

@register.simple_tag
def cart_quantity(user):
    try:
        cart_product_count = CartProduct.objects.filter(cart__buyer__user=user).count()
        return cart_product_count
    except CartProduct.DoesNotExist:
        return 0
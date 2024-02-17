from django.shortcuts import render
from products.views import all_products
from products.models import Product, Category,CartProduct,Cart
from accounts.models import Profile
import random
from django.contrib.auth.decorators import login_required  
from django.shortcuts import render, get_object_or_404, redirect

@login_required
def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    todaysdeal = random.sample(list(products), 3)
    youmighlike = random.sample(list(products), 3)
    user = request.user
    buyer_profile = get_object_or_404(Profile, user=request.user)
    print(buyer_profile)
    if buyer_profile is not None:
        try:
            cart = Cart.objects.get(buyer=buyer_profile)
            if cart:
                cart_counts = CartProduct.cart_count(cart)
        except Cart.DoesNotExist:
            cart_counts = 0

    context = {'products': products, 'categories': categories, 'todaysdeal': todaysdeal, 'youmighlike': youmighlike,
               "user": user, "cart_counts": cart_counts}
    return render(request, 'pages/hero.html', context)




def about(request):
    return render(request,'pages/about.html')

def getting_start(request):
    return render(request,'pages/getting_start.html')

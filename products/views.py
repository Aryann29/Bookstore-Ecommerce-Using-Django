from django.shortcuts import render,HttpResponse
from .models import Product, Category
import random
from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import Profile
from accounts.views import add_to_cart

def all_products(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request,'products.html',{'products' : products , 'categories':categories})



def product_detail(request, slug):

    product = get_object_or_404(Product, slug=slug)
   
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        print(quantity)
        buyer_profile = get_object_or_404(Profile, user=request.user)
        add_to_cart(request, product,quantity,  buyer_profile)
        return redirect('product_detail', slug=slug)
    
    context = {
        'product': product,
    }

    return render(request, 'product_detail.html', context)
   
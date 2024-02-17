from django.shortcuts import render,redirect,HttpResponseRedirect
from .models import Profile
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from products.models import Product,Cart,CartProduct
from django.shortcuts import get_object_or_404

def login_page(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)

        if not user_obj.exists():
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)


        user_obj = authenticate(username = email , password= password)
        if user_obj:
            login(request , user_obj)
            return redirect('/')

        

        messages.warning(request, 'Invalid credentials')
        return HttpResponseRedirect(request.path_info)


    return render(request ,'accounts/login.html')


def signup(request):

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)

        if user_obj.exists():
            messages.warning(request, 'Email is already taken.')
            return HttpResponseRedirect(request.path_info)

        print(email)

        user_obj = User.objects.create(first_name = first_name , last_name= last_name , email = email , username = email)
        user_obj.set_password(password)
        user_obj.save()
        profile_obj = Profile.objects.create(user=user_obj, is_seller=False, bio='')
        return HttpResponseRedirect(request.path_info)
    return render(request,'accounts/register.html')


def logout_page(request):
    return redirect('getting_start')

@login_required
def edit(request):
    user = request.user  
    
    if request.method == 'POST':
        updated_first_name = request.POST.get('first_name')
        updated_last_name = request.POST.get('last_name')
        updated_bio = request.POST.get('bio')

        user_profile = Profile.objects.get(user=user)

        
        user_profile.first_name = updated_first_name
        user_profile.last_name = updated_last_name
        user_profile.bio = updated_bio
        user_profile.save()
        
        return redirect('edit')

    return render(request, 'accounts/edit.html', {'user': user})


@login_required
def my_products_page(request):
    user = request.user
    products = Product.objects.filter(seller=user.profile)
    return render(request, 'accounts/my_products.html', {'user': user, 'products': products})

def orders_page(request):
    return render(request,'accounts/orders.html')

def changepswd(request):
    return render(request,'accounts/changepswd.html')

@login_required
def cart(request):
    user = request.user
    profile = user.profile

    try:
        cart = profile.cart
        cart_products = CartProduct.objects.filter(cart=cart)
        subtotal =  calc_total(cart_products)    
    except Cart.DoesNotExist:
        cart_products = None
        
    context = {'cart_products': cart_products , 'subtotal': subtotal}
    return render(request, 'accounts/cart.html', context)


from django.contrib import messages

@login_required
def add_to_cart(request, product, quantity, buyer_profile):
    cart, created = Cart.objects.get_or_create(buyer=buyer_profile)
    cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product, defaults={'quantity': quantity})

    if not created:
        cart_product.quantity += quantity
        cart_product.save()
        messages.success(request, f"{quantity} x {product.product_name} added to cart for {buyer_profile.user.username}")
    else:
        messages.error(request, "Error adding to cart.")

    return redirect('product_detail', slug=product.slug)



def remove_from_cart():
    pass


def calc_total(products):
    total = 0
    for product in products:
        total += product.total_price
    return total

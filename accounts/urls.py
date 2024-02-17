from django.urls import path,include
from . import views

urlpatterns = [
    path('login/', views.login_page,name='login_page'),
    path('signup/', views.signup,name='signup'),
    path('edit/', views.edit,name='edit'),
    path('change-password/', views.changepswd,name='changepswd'),
    path('orders/', views.orders_page,name='orders_page'),
    path('my_products/', views.my_products_page,name='my_products_page'),
    path('cart/', views.cart, name='cart'),
]

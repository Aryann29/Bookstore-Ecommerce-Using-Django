from django.urls import path
from . import views



urlpatterns = [
    path('', views.home,name='hero'),
    path('about', views.about,name='about'),
    path('getting_start', views.getting_start,name='getting_start'),
    
]



from django.contrib import admin
from .models import Category, Product,CartProduct,ProductImages,Cart



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'seller', 'category', 'price')
    prepopulated_fields = {'slug': ('product_name',)}

@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'images')
    
class CartProductInline(admin.TabularInline):
    model = CartProduct
    extra = 1
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('buyer',)
    inlines = [CartProductInline]
@admin.register(CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'total_price')


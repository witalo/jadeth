from django.contrib import admin

from apps.products.models import Product, ProductModel, ProductBrand, Color

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductBrand)
admin.site.register(ProductModel)
admin.site.register(Color)

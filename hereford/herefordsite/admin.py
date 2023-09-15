from django.contrib import admin
from .models import ProductType, SubProductType, Product, CarouselImage


class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

class SubProductTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'product_type')
    search_fields = ('name',)
    list_filter = ('product_type',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_type', 'sub_product_type', 'region', 'farm', 'contact_phone', 'age', 'price', 'product_photo')
    search_fields = ('product_type__name', 'sub_product_type__name', 'region', 'farm')
    list_filter = ('product_type', 'sub_product_type')


admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(SubProductType, SubProductTypeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(CarouselImage)

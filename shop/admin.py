from django.contrib import admin
from django.utils.safestring import mark_safe

# Register your models here.
from .models import Subcategory, Category, Product, Color, Region, City, ShippingAddress


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', 'created')
    list_display_links = ('pk', 'name')

    prepopulated_fields = {'slug': ('name',)}


@admin.register(Subcategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'category', 'slug', 'created', 'get_image')
    list_display_links = ('pk', 'name')

    def get_image(self, product):
        if product.image:
            return mark_safe(f'<img src="{product.image.url}" width="75px" style="border-radius: 15px;">')
        else:
            return 'Image not found'

    prepopulated_fields = {'slug': ('name', 'category')}
    get_image.short_description = 'Image'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'price', 'quantity', 'color', 'created', 'get_image')

    def get_image(self, product):
        if product.image:
            return mark_safe(f'<img src="{product.image.url}" width="75px" style="border-radius: 15px;">')
        else:
            return 'Image not found'

    get_image.short_description = 'Image'


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'created')


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'region')


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('pk', 'customer', 'order', 'address', 'region', 'city', 'zip_code', 'mobile', 'email')

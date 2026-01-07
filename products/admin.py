from django.contrib import admin
from .models import Product, ProductImage, Feature


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'alt']


class FeatureInline(admin.TabularInline):
    model = Feature
    extra = 1
    fields = ('name', 'value')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')
    inlines = [ProductImageInline, FeatureInline]

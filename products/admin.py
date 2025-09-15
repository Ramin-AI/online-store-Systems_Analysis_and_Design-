from django.contrib import admin
from django.utils.html import format_html
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Product model.
    """
    list_display = ('name', 'price', 'category', 'inventory', 'image_preview')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    ordering = ('name',)
    readonly_fields = ('image_preview_large',)
    fields = ('name', 'description', 'price', 'category', 'inventory', 'image', 'image_preview_large')
    
    def image_preview(self, obj):
        """Display a small thumbnail in the admin list view"""
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: contain;" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Image'
    
    def image_preview_large(self, obj):
        """Display a larger image preview in the detail view"""
        if obj.image:
            return format_html('<img src="{}" width="300" height="300" style="object-fit: contain;" />', obj.image.url)
        return "-"
    image_preview_large.short_description = 'Image Preview'
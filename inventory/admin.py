from django.contrib import admin
from .models import InventoryItem, Category


@admin.register(InventoryItem)
class ItemsAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "unit_price", "slug", "sku", "is_active"]


@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ["name", "is_active"]

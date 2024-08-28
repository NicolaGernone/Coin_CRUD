from .models import Cart, CartItem
import django.contrib.admin as admin


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "hash", "items")


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "quantity", "price", "previous_hash", "hash")
    list_filter = ["cart"]
    search_fields = ["name"]

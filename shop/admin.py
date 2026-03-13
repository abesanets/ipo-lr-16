from django.contrib import admin
from .models import Category, Manufacturer, Product, Cart, CartItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country')
    search_fields = ('name', 'country')
    list_filter = ('country',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'stock', 'category', 'manufacturer')
    search_fields = ('name',)
    list_filter = ('category', 'manufacturer')
    list_editable = ('price', 'stock')


class CartItemInline(admin.TabularInline):
    """Позволяет редактировать элементы корзины прямо на странице корзины"""
    model = CartItem
    extra = 1
    readonly_fields = ('item_cost',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'total_cost')
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity', 'item_cost')
    list_filter = ('cart',)

from .models import Category, Manufacturer, Product, Cart, CartItem, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'product_price', 'quantity', 'item_cost')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone', 'email', 'total_cost', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'email', 'phone')
    readonly_fields = ('created_at',)
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product_name', 'product_price', 'quantity', 'item_cost')
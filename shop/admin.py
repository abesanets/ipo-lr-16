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

    def has_module_permission(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser or (hasattr(request.user, 'profile') and request.user.profile.role in ['ADMIN', 'MANAGER']):
                return True
        return super().has_module_permission(request)

    def has_view_permission(self, request, obj=None):
        if request.user.is_authenticated:
            if request.user.is_superuser or (hasattr(request.user, 'profile') and request.user.profile.role in ['ADMIN', 'MANAGER']):
                return True
        return super().has_view_permission(request, obj)

    def has_change_permission(self, request, obj=None):
        if request.user.is_authenticated:
            if request.user.is_superuser or (hasattr(request.user, 'profile') and request.user.profile.role in ['ADMIN', 'MANAGER']):
                return True
        return super().has_change_permission(request, obj)

    def has_add_permission(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser or (hasattr(request.user, 'profile') and request.user.profile.role in ['ADMIN', 'MANAGER']):
                return True
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_authenticated:
            if request.user.is_superuser or (hasattr(request.user, 'profile') and request.user.profile.role in ['ADMIN', 'MANAGER']):
                return True
        return super().has_delete_permission(request, obj)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product_name', 'product_price', 'quantity', 'item_cost')

    def has_module_permission(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser or (hasattr(request.user, 'profile') and request.user.profile.role in ['ADMIN', 'MANAGER']):
                return True
        return super().has_module_permission(request)

    def has_view_permission(self, request, obj=None):
        if request.user.is_authenticated:
            if request.user.is_superuser or (hasattr(request.user, 'profile') and request.user.profile.role in ['ADMIN', 'MANAGER']):
                return True
        return super().has_view_permission(request, obj)

    def has_change_permission(self, request, obj=None):
        if request.user.is_authenticated:
            if request.user.is_superuser or (hasattr(request.user, 'profile') and request.user.profile.role in ['ADMIN', 'MANAGER']):
                return True
        return super().has_change_permission(request, obj)

    def has_add_permission(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser or (hasattr(request.user, 'profile') and request.user.profile.role in ['ADMIN', 'MANAGER']):
                return True
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_authenticated:
            if request.user.is_superuser or (hasattr(request.user, 'profile') and request.user.profile.role in ['ADMIN', 'MANAGER']):
                return True
        return super().has_delete_permission(request, obj)


from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'role', 'full_name', 'phone', 'delivery_city')
    list_filter = ('role', 'delivery_city')
    search_fields = ('user__username', 'full_name', 'phone')
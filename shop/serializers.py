from rest_framework import serializers
from .models import Category, Manufacturer, Product, Cart, CartItem, Order, OrderItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    # Вложенные объекты только для чтения
    category_name = serializers.CharField(source='category.name', read_only=True)
    manufacturer_name = serializers.CharField(source='manufacturer.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'image',
                  'category', 'category_name', 'manufacturer', 'manufacturer_name']


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    cost = serializers.DecimalField(source='item_cost', max_digits=12,
                                    decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'product_name', 'quantity', 'cost']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.DecimalField(source='total_cost', max_digits=12,
                                     decimal_places=2, read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'username', 'created_at', 'items', 'total']


class OrderItemSerializer(serializers.ModelSerializer):
    cost = serializers.DecimalField(source='item_cost', max_digits=12,
                                    decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product_name', 'product_price', 'quantity', 'cost']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'username', 'address', 'phone', 'email',
                  'created_at', 'total_cost', 'items']

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


from .models import Profile

import re

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id', 'username', 'email', 'full_name', 'phone', 'address', 
            'role', 'role_display', 'delivery_city', 'postal_code'
        ]
        read_only_fields = ['id', 'role']

    def validate_full_name(self, value):
        value = value.strip()
        if not value:
            return value
        if len(value) > 100:
            raise serializers.ValidationError("ФИО не должно превышать 100 символов.")
        if not re.match(r'^[a-zA-Zа-яА-ЯёЁ\s\-]+$', value):
            raise serializers.ValidationError("ФИО должно содержать только буквы, пробелы и дефисы.")
        words = value.split()
        if len(words) < 2:
            raise serializers.ValidationError("Пожалуйста, введите фамилию и имя.")
        return value

    def validate_phone(self, value):
        value = value.strip()
        if not value:
            return value
        if not re.match(r'^\+?[0-9\s\-\(\)]{7,20}$', value):
            raise serializers.ValidationError("Неверный формат номера телефона. Введите от 7 до 20 цифр/знаков.")
        return value

    def validate_delivery_city(self, value):
        value = value.strip()
        if not value:
            return value
        if len(value) > 50:
            raise serializers.ValidationError("Название города не должно превышать 50 символов.")
        if not re.match(r'^[a-zA-Zа-яА-ЯёЁ\s\-]+$', value):
            raise serializers.ValidationError("Название города должно содержать только буквы, пробелы и дефисы.")
        return value

    def validate_postal_code(self, value):
        value = value.strip()
        if not value:
            return value
        if not re.match(r'^\d{5,6}$', value):
            raise serializers.ValidationError("Индекс должен состоять ровно из 5 или 6 цифр.")
        return value

    def validate_address(self, value):
        value = value.strip()
        if not value:
            return value
        if len(value) > 200:
            raise serializers.ValidationError("Адрес не должен превышать 200 символов.")
        if len(value) < 5:
            raise serializers.ValidationError("Пожалуйста, укажите адрес подробнее (улица, дом).")
        return value


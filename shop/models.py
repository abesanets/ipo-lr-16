from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User


# ==================== ЗАДАНИЕ 1 ====================

class Category(models.Model):
    """Модель категории товара"""
    name = models.CharField(
        max_length=100,
        verbose_name='Название'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    """Модель производителя"""
    name = models.CharField(
        max_length=100,
        verbose_name='Название'
    )
    country = models.CharField(
        max_length=100,
        verbose_name='Страна'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель товара"""
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    image = models.ImageField(
        upload_to='products/',
        verbose_name='Фото товара',
        blank=True,
        null=True
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Цена'
    )
    stock = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name='Количество на складе'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Категория'
    )
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Производитель'
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


# ==================== ЗАДАНИЕ 2 ====================

class Cart(models.Model):
    """Модель корзины"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"

    def total_cost(self):
        """Общая стоимость всех элементов корзины"""
        return sum(item.item_cost() for item in self.items.all())

    total_cost.short_description = 'Общая стоимость'


class CartItem(models.Model):
    """Модель элемента корзины"""
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Корзина'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name='Товар'
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'

    def __str__(self):
        return f"{self.product.name} ({self.quantity} шт.)"

    def item_cost(self):
        """Стоимость элемента = цена * количество"""
        return self.product.price * self.quantity

    item_cost.short_description = 'Стоимость'

    def clean(self):
        """Валидация: количество не должно превышать остаток на складе"""
        from django.core.exceptions import ValidationError
        if self.quantity and self.product and self.quantity > self.product.stock:
            raise ValidationError(
                f'Количество ({self.quantity}) превышает остаток на складе ({self.product.stock})'
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class Order(models.Model):
    """Модель заказа"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Пользователь'
    )
    address = models.TextField(
        verbose_name='Адрес доставки'
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='Телефон'
    )
    email = models.EmailField(
        verbose_name='Email для чека'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата заказа'
    )
    total_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Общая стоимость'
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ #{self.id} от {self.user.username}"


class OrderItem(models.Model):
    """Модель элемента заказа"""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ'
    )
    product_name = models.CharField(
        max_length=200,
        verbose_name='Название товара'
    )
    product_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена'
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'

    def __str__(self):
        return f"{self.product_name} ({self.quantity} шт.)"

    def item_cost(self):
        return self.product_price * self.quantity

    item_cost.short_description = 'Стоимость'


# ==================== ЗАДАНИЕ 1: ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ ====================

class Profile(models.Model):
    """Модель профиля пользователя с ролями"""
    ROLE_CHOICES = [
        ('CUSTOMER', 'Покупатель'),
        ('MANAGER', 'Менеджер'),
        ('ADMIN', 'Администратор'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='CUSTOMER',
        verbose_name='Роль'
    )
    full_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='ФИО'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Телефон'
    )
    address = models.TextField(
        blank=True,
        verbose_name='Адрес доставки'
    )
    # Индивидуальные поля для лабораторной работы
    delivery_city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Город доставки'
    )
    postal_code = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Индекс'
    )

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return f"Профиль {self.user.username} ({self.get_role_display()})"


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Profile)
def sync_user_staff_status(sender, instance, **kwargs):
    """Синхронизирует флаг is_staff пользователя в зависимости от его роли в профиле"""
    is_privileged = instance.role in ['ADMIN', 'MANAGER']
    user = instance.user
    if is_privileged and not user.is_staff:
        user.is_staff = True
        user.save()
    elif not is_privileged and user.is_staff and not user.is_superuser:
        user.is_staff = False
        user.save()
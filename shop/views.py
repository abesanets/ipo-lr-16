from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import StyledUserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q

from .models import Product, Category, Manufacturer, Cart, CartItem


# ==================== ОСНОВНЫЕ СТРАНИЦЫ ====================

def index(request):
    """Главная страница"""
    categories = Category.objects.all()
    latest_products = Product.objects.select_related('category', 'manufacturer').order_by('-id')[:8]
    return render(request, 'shop/index.html', {
        'categories': categories,
        'latest_products': latest_products,
    })


def about(request):
    """Страница об авторе"""
    return render(request, 'shop/about.html')


def shop_info(request):
    """Страница о магазине"""
    return render(request, 'shop/shop_info.html', {
        'categories_count': Category.objects.count(),
        'products_count': Product.objects.count(),
        'manufacturers_count': Manufacturer.objects.count(),
    })


# ==================== КАТАЛОГ ====================

def product_list(request):
    """Список товаров с фильтрацией, поиском и сортировкой"""
    products = Product.objects.select_related('category', 'manufacturer').all()

    # Поиск по названию и описанию (Q-объекты)
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Фильтр по категории
    selected_category = request.GET.get('category', '')
    if selected_category:
        products = products.filter(category__id=selected_category)

    # Фильтр по производителю
    selected_manufacturer = request.GET.get('manufacturer', '')
    if selected_manufacturer:
        products = products.filter(manufacturer__id=selected_manufacturer)

    # Фильтр по цене
    price_min = request.GET.get('price_min', '')
    if price_min:
        products = products.filter(price__gte=price_min)

    price_max = request.GET.get('price_max', '')
    if price_max:
        products = products.filter(price__lte=price_max)

    # Сортировка
    sort = request.GET.get('sort', 'name')
    valid_sorts = ['name', '-name', 'price', '-price', '-stock']
    if sort in valid_sorts:
        products = products.order_by(sort)

    context = {
        'products': products,
        'categories': Category.objects.all(),
        'manufacturers': Manufacturer.objects.all(),
        'search_query': search_query,
        'selected_category': selected_category,
        'selected_manufacturer': selected_manufacturer,
        'price_min': price_min,
        'price_max': price_max,
        'sort': sort,
    }
    return render(request, 'shop/product_list.html', context)


def product_detail(request, pk):
    """Детальная страница товара"""
    product = get_object_or_404(
        Product.objects.select_related('category', 'manufacturer'),
        pk=pk
    )
    return render(request, 'shop/product_detail.html', {
        'product': product,
    })


# ==================== КОРЗИНА ====================

@login_required
def cart_view(request):
    """Просмотр корзины пользователя"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product', 'product__manufacturer').all()

    total_cost = cart.total_cost()

    return render(request, 'shop/cart.html', {
        'cart': cart,
        'items': items,
        'total_cost': total_cost,
    })


@login_required
def add_to_cart(request, product_id):
    """Добавление товара в корзину"""
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)

        quantity = int(request.POST.get('quantity', 1))

        # Проверка наличия на складе
        if quantity > product.stock:
            messages.error(
                request,
                f'Недостаточно товара на складе. Доступно: {product.stock} шт.'
            )
            return redirect('product_detail', pk=product_id)

        # Проверяем, есть ли уже этот товар в корзине
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )

        if not item_created:
            # Товар уже в корзине — увеличиваем количество
            new_quantity = cart_item.quantity + quantity
            if new_quantity > product.stock:
                messages.error(
                    request,
                    f'Недостаточно товара на складе. В корзине: {cart_item.quantity}, '
                    f'доступно всего: {product.stock} шт.'
                )
                return redirect('product_detail', pk=product_id)

            cart_item.quantity = new_quantity
            cart_item.save()
            messages.success(request, f'Количество "{product.name}" обновлено в корзине.')
        else:
            messages.success(request, f'"{product.name}" добавлен в корзину.')

    return redirect('cart_view')


@login_required
def update_cart(request, item_id):
    """Обновление количества товара в корзине"""
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        new_quantity = int(request.POST.get('quantity', 1))

        if new_quantity <= 0:
            cart_item.delete()
            messages.success(request, f'"{cart_item.product.name}" удалён из корзины.')
        elif new_quantity > cart_item.product.stock:
            messages.error(
                request,
                f'Недостаточно товара на складе. Доступно: {cart_item.product.stock} шт.'
            )
        else:
            cart_item.quantity = new_quantity
            cart_item.save()
            messages.success(request, f'Количество "{cart_item.product.name}" обновлено.')

    return redirect('cart_view')


@login_required
def remove_from_cart(request, item_id):
    """Удаление товара из корзины"""
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        product_name = cart_item.product.name
        cart_item.delete()
        messages.success(request, f'"{product_name}" удалён из корзины.')

    return redirect('cart_view')


# ==================== АУТЕНТИФИКАЦИЯ ====================

def register(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = StyledUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Cart.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('index')
    else:
        form = StyledUserCreationForm()

    return render(request, 'shop/register.html', {'form': form})
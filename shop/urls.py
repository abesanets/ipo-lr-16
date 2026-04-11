from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from . import views

# ==================== DRF ROUTER ====================
router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'manufacturers', views.ManufacturerViewSet, basename='manufacturer')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'carts', views.CartViewSet, basename='cart')
router.register(r'cart-items', views.CartItemViewSet, basename='cartitem')
router.register(r'orders', views.OrderViewSet, basename='order')
router.register(r'order-items', views.OrderItemViewSet, basename='orderitem')

urlpatterns = [
    # API маршруты
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),  # логин/логаут для browsable API

    # Основные страницы
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('shop-info/', views.shop_info, name='shop_info'),

    # Каталог
    path('catalog/', views.product_list, name='product_list'),
    path('catalog/<int:pk>/', views.product_detail, name='product_detail'),

    # Корзина
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Оформление заказа
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),

    # Аутентификация
    path('login/', auth_views.LoginView.as_view(
        template_name='shop/login.html',
        redirect_authenticated_user=True,
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]
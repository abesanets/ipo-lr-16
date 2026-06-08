# Интернет-магазин электроники — Shopex

## Описание

Учебный проект на Django, созданный в рамках лабораторных работ №16–23.
Полнофункциональный интернет-магазин электроники с каталогом товаров, корзиной,
системой аутентификации, оформлением заказов, REST API и адаптивным клиентским интерфейсом.

---

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/abesanets/ipo-lr-16
```

### 2. Создание и активация виртуального окружения

```bash
python -m venv venv
venv\Scripts\activate
```
### 3. Установка зависимостей

```bash
pip install django djangorestframework Pillow openpyxl
```

### 4. Настройка email

В `shop_project/settings.py` замените на свои данные:

```python
EMAIL_HOST_USER = 'ваша_почта@gmail.com'
EMAIL_HOST_PASSWORD = 'пароль_приложения'  # 16-символьный пароль приложения Gmail
DEFAULT_FROM_EMAIL = 'ваша_почта@gmail.com'
```

Для тестирования без отправки писем:
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### 5. Применение миграций и запуск

```bash
python manage.py migrate
python manage.py runserver
```

Откройте: **http://127.0.0.1:8000/**

---

## Тестовые данные

**Суперпользователь:**
- Логин: `admin` / Пароль: `admin123`
- Админ-панель: http://127.0.0.1:8000/admin/

**Тестовые пользователи:** `ivan`, `maria`, `alex`, `elena`, `dmitry` — пароль `userpass123`

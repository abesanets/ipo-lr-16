// Получение CSRF-токена из cookie
function getCsrfToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [key, value] = cookie.trim().split('=');
        if (key === name) return decodeURIComponent(value);
    }
    return '';
}

// Показать Bootstrap Toast с сообщением
function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const id = 'toast-' + Date.now();
    const bgClass = type === 'success' ? 'bg-success' : 'bg-danger';

    container.insertAdjacentHTML('beforeend', `
        <div id="${id}" class="toast align-items-center text-white ${bgClass} border-0" role="alert" aria-live="assertive">
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `);

    const toastEl = document.getElementById(id);
    const toast = new bootstrap.Toast(toastEl, { delay: 3000 });
    toast.show();
    toastEl.addEventListener('hidden.bs.toast', () => toastEl.remove());
}

// Загрузка товаров из API и динамический рендеринг
function loadProducts(containerId, apiUrl = '/api/products/') {
    const container = document.getElementById(containerId);
    const spinner = document.getElementById('loading-spinner');

    if (!container) return;

    if (spinner) spinner.style.display = 'block';
    container.innerHTML = '';

    fetch(apiUrl)
        .then(response => {
            if (response.status === 403 || response.status === 401) {
                throw new Error('Для загрузки товаров через API необходимо войти в аккаунт.');
            }
            if (!response.ok) throw new Error(`Ошибка сервера: ${response.status}`);
            return response.json();
        })
        .then(data => {
            if (spinner) spinner.style.display = 'none';

            // DRF возвращает либо массив, либо объект с results (при пагинации)
            const products = Array.isArray(data) ? data : (data.results || []);

            if (products.length === 0) {
                container.innerHTML = '<p class="text-muted">Товары не найдены.</p>';
                return;
            }

            container.innerHTML = '';
            // Проверяем авторизацию пользователя по наличию кнопки "Выйти" в шапке
            const isAuthenticated = !!document.querySelector('.btn-nav-logout');

            products.forEach(product => {
                let cartBtn = '';
                if (product.stock === 0) {
                    cartBtn = `<span class="stock-badge out">Нет в наличии</span>`;
                } else if (isAuthenticated) {
                    cartBtn = `<button class="btn btn-primary btn-sm" onclick="addToCart(${product.id}, '${product.name}')">В корзину</button>`;
                } else {
                    cartBtn = `<a href="/login/?next=/catalog/" class="btn btn-ghost btn-sm">Войти</a>`;
                }

                container.innerHTML += `
                    <div class="product-card">
                        <div class="product-card-body">
                            <div class="product-card-category">${product.category_name || ''}</div>
                            <div class="product-card-name">
                                <a href="/catalog/${product.id}/">${product.name}</a>
                            </div>
                            <div class="product-card-mfr">${product.manufacturer_name || ''}</div>
                        </div>
                        <div class="product-card-footer">
                            <span class="price">${product.price} Br</span>
                            ${cartBtn}
                        </div>
                    </div>`;
            });
        })
        .catch(error => {
            if (spinner) spinner.style.display = 'none';
            console.error('Ошибка загрузки товаров:', error);
            if (container) {
                container.innerHTML = `
                    <div class="col-12">
                        <div class="alert alert-danger">
                            ${error.message || 'Не удалось загрузить товары. Попробуйте обновить страницу.'}
                        </div>
                    </div>`;
            }
        });
}

// Добавление товара в корзину через API
function addToCart(productId, productName = 'Товар', quantity = 1) {
    fetch(`/cart/add/${productId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCsrfToken(),
        },
        body: `quantity=${quantity}`,
    })
        .then(response => {
            if (response.redirected || response.ok) {
                showToast(`"${productName}" добавлен в корзину`, 'success');
            } else {
                throw new Error('Ошибка при добавлении');
            }
        })
        .catch(error => {
            console.error('Ошибка добавления в корзину:', error);
            showToast('Не удалось добавить товар в корзину', 'danger');
        });
}

// Делегирование кликов для всей карточки товара (за исключением интерактивных элементов)
document.addEventListener('DOMContentLoaded', () => {
    document.body.addEventListener('click', (e) => {
        const card = e.target.closest('.product-card');
        if (!card) return;

        // Если кликнули по кнопке, форме или ссылке внутри карточки — ничего не делаем
        if (e.target.closest('button') || e.target.closest('form') || e.target.closest('a')) {
            return;
        }

        // Ищем ссылку на детальную страницу товара и переходим по ней
        const link = card.querySelector('.product-card-img-link') || card.querySelector('.product-card-name a');
        if (link) {
            window.location.href = link.href;
        }
    });
});


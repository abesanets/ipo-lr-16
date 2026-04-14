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
            products.forEach(product => {
                const imgHtml = product.image
                    ? `<img src="${product.image}" class="card-img-top product-card-img" alt="${product.name}">`
                    : `<div class="card-img-top product-card-img bg-light d-flex align-items-center justify-content-center">
                           <svg width="48" height="48" fill="none" stroke="#aaa" stroke-width="1.5" viewBox="0 0 24 24"><rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/></svg>
                       </div>`;

                const cartBtn = product.stock > 0
                    ? `<button class="btn btn-primary btn-sm" onclick="addToCart(${product.id}, '${product.name}')">В корзину</button>`
                    : `<button class="btn btn-secondary btn-sm" disabled>Нет в наличии</button>`;

                container.innerHTML += `
                    <div class="col-sm-6 col-md-4 col-lg-4 mb-4">
                        <div class="card h-100 product-card shadow-sm">
                            <a href="/catalog/${product.id}/">${imgHtml}</a>
                            <div class="card-body">
                                <p class="text-muted small mb-1">${product.category_name || ''}</p>
                                <h5 class="card-title">
                                    <a href="/catalog/${product.id}/" class="text-decoration-none text-dark">${product.name}</a>
                                </h5>
                                <p class="text-muted small">${product.manufacturer_name || ''}</p>
                            </div>
                            <div class="card-footer d-flex justify-content-between align-items-center">
                                <span class="fw-bold fs-5">${product.price} ₽</span>
                                ${cartBtn}
                            </div>
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
